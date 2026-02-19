from __future__ import annotations

import math
import re
from collections import Counter
from statistics import mean

from sklearn.feature_extraction.text import TfidfVectorizer

from backend.models.schemas import ATSResult, ResumeData

ACTION_VERBS = {
    "led", "built", "created", "improved", "designed", "implemented", "managed", "optimized",
    "developed", "launched", "delivered", "coordinated", "analyzed", "streamlined", "executed",
}
PERSONAL_PRONOUNS = {"i", "me", "my", "mine", "we", "our", "ours"}
COMMON_ROLE_KEYWORDS = {
    "software": ["python", "api", "microservices", "docker", "cloud", "sql", "agile"],
    "data": ["sql", "python", "pandas", "machine learning", "analytics", "dashboard", "etl"],
    "product": ["roadmap", "kpi", "stakeholders", "go-to-market", "experiments", "strategy"],
}
DATE_PATTERN = re.compile(r"^(\w+\s+\d{4}|\d{4})(\s*[-–]\s*(Present|\w+\s+\d{4}|\d{4}))?$")


class ATSScorerService:
    @staticmethod
    def _resume_text(resume: ResumeData) -> str:
        chunks = [
            resume.personal_info.name,
            resume.summary or "",
            " ".join(resume.skills),
            " ".join(resume.certifications),
        ]
        for edu in resume.education:
            chunks.append(f"{edu.degree} {edu.institution} {edu.year} {' '.join(edu.relevant_courses)}")
        for exp in resume.experience:
            chunks.append(f"{exp.title} {exp.company} {' '.join(exp.bullets)}")
        for proj in resume.projects:
            chunks.append(f"{proj.name} {proj.description} {' '.join(proj.tech_stack)}")
        return "\n".join(chunks).lower()

    @staticmethod
    def _extract_keywords(job_description: str) -> list[str]:
        tokens = re.findall(r"[a-zA-Z][a-zA-Z+.#-]{1,}", job_description.lower())
        stopwords = {
            "the", "and", "for", "with", "you", "your", "our", "that", "this", "are", "from",
            "have", "will", "into", "work", "team", "role", "years", "experience", "required",
        }
        return [t for t in tokens if t not in stopwords]

    @staticmethod
    def _detect_role(resume: ResumeData) -> str:
        titles = " ".join(exp.title.lower() for exp in resume.experience)
        if any(word in titles for word in ["data", "analyst", "scientist"]):
            return "data"
        if any(word in titles for word in ["product", "pm"]):
            return "product"
        return "software"

    def keyword_score(self, resume: ResumeData, job_description: str | None) -> tuple[int, list[str]]:
        resume_text = self._resume_text(resume)
        if job_description and job_description.strip():
            keywords = self._extract_keywords(job_description)
        else:
            keywords = COMMON_ROLE_KEYWORDS[self._detect_role(resume)]

        if not keywords:
            return 20, []

        docs = [" ".join(keywords), resume_text]
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        matrix = vectorizer.fit_transform(docs)
        jd_vector = matrix[0]
        resume_vector = matrix[1]

        jd_weights = {term: jd_vector[0, idx] for term, idx in vectorizer.vocabulary_.items() if jd_vector[0, idx] > 0}
        total_weight = sum(jd_weights.values()) or 1.0

        matched_weight = 0.0
        missing_keywords: list[str] = []
        for term, weight in jd_weights.items():
            if resume_vector[0, vectorizer.vocabulary_[term]] > 0:
                matched_weight += weight
            else:
                missing_keywords.append(term)

        ratio = matched_weight / total_weight
        return int(round(40 * ratio)), missing_keywords[:20]

    @staticmethod
    def section_score(resume: ResumeData) -> tuple[int, list[str]]:
        suggestions: list[str] = []
        score = 20
        sections = {
            "summary": bool(resume.summary and resume.summary.strip()),
            "education": len(resume.education) > 0,
            "skills": len(resume.skills) > 0,
            "experience": len(resume.experience) > 0,
            "projects": len(resume.projects) > 0,
        }
        missing = [name for name, present in sections.items() if not present]
        if missing:
            deduction = math.ceil(20 / len(sections))
            score -= deduction * len(missing)
            suggestions.append(f"Add or expand these sections: {', '.join(missing)}.")
        return max(0, score), suggestions

    @staticmethod
    def formatting_score(resume: ResumeData) -> tuple[int, list[str]]:
        suggestions: list[str] = []
        score = 20
        bullets = [b for exp in resume.experience for b in exp.bullets]

        if bullets:
            action_hits = sum(1 for b in bullets if b.split() and b.split()[0].lower().strip(".,") in ACTION_VERBS)
            action_ratio = action_hits / len(bullets)
            if action_ratio < 0.6:
                score -= 6
                suggestions.append("Start more bullets with strong action verbs.")

            lengths = [len(re.findall(r"\w+", b)) for b in bullets]
            in_range = sum(1 for l in lengths if 15 <= l <= 30)
            if in_range / len(lengths) < 0.6:
                score -= 6
                suggestions.append("Keep bullet length mostly between 15 and 30 words.")

            pronoun_hits = sum(1 for b in bullets if set(re.findall(r"\b\w+\b", b.lower())) & PERSONAL_PRONOUNS)
            if pronoun_hits > 0:
                score -= 4
                suggestions.append("Avoid personal pronouns in experience bullets.")

        date_consistency_fail = any(
            not DATE_PATTERN.match(f"{exp.start_date} - {exp.end_date}".strip()) for exp in resume.experience
        )
        if date_consistency_fail:
            score -= 4
            suggestions.append("Use consistent date formats (e.g., Jan 2021 - Mar 2023).")

        return max(0, score), suggestions

    @staticmethod
    def readability_score(resume: ResumeData) -> tuple[int, list[str]]:
        suggestions: list[str] = []
        score = 20
        text = ATSScorerService._resume_text(resume)
        sentences = re.split(r"[.!?\n]+", text)
        sentences = [s.strip() for s in sentences if s.strip()]
        words = re.findall(r"\b\w+\b", text)
        syllables = sum(max(1, len(re.findall(r"[aeiouy]+", w.lower()))) for w in words)

        if not words or not sentences:
            return 10, ["Add richer content to improve readability analysis."]

        words_per_sentence = len(words) / len(sentences)
        flesch = 206.835 - 1.015 * words_per_sentence - 84.6 * (syllables / len(words))

        if flesch < 35:
            score -= 8
            suggestions.append("Simplify sentence construction for better readability.")

        lengths = [len(re.findall(r"\w+", s)) for s in sentences]
        if lengths:
            variability = (max(lengths) - min(lengths)) / max(1, mean(lengths))
            if variability < 0.4:
                score -= 5
                suggestions.append("Vary sentence lengths to improve flow.")

        jargon_terms = [w for w, c in Counter(words).items() if c >= 4 and len(w) > 10]
        jargon_density = len(jargon_terms) / max(1, len(set(words)))
        if jargon_density > 0.08:
            score -= 7
            suggestions.append("Reduce repeated jargon-heavy terms.")

        return max(0, score), suggestions

    def score_resume(self, resume: ResumeData, job_description: str | None = None) -> ATSResult:
        k_score, missing_keywords = self.keyword_score(resume, job_description)
        s_score, section_suggestions = self.section_score(resume)
        f_score, formatting_suggestions = self.formatting_score(resume)
        r_score, readability_suggestions = self.readability_score(resume)

        overall = max(0, min(100, k_score + s_score + f_score + r_score))
        suggestions = section_suggestions + formatting_suggestions + readability_suggestions
        if missing_keywords:
            suggestions.append("Include missing keywords where relevant to your experience.")

        return ATSResult(
            overall_score=overall,
            keyword_score=k_score,
            section_score=s_score,
            formatting_score=f_score,
            readability_score=r_score,
            missing_keywords=missing_keywords,
            suggestions=suggestions[:15],
        )


ats_scorer_service = ATSScorerService()
