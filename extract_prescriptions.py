#!/usr/bin/env python3
"""Robust prescription text extractor.

This script reads JSON data containing raw prescription text and writes a
structured JSON output with fields:
  medicine_name, form, strength, dosage, frequency, duration, notes

Supported input shapes:
1) [{"raw_text": "..."}, ...]
2) {"records": [{"raw_text": "..."}, ...]} (or any nested containers)
3) ["raw text 1", "raw text 2", ...]

Usage:
  python extract_prescriptions.py --input prescription_raw_text_only.json --output prescription_structured_output.json
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

# ---------- Normalization dictionaries ----------
FORM_ALIASES: List[Tuple[str, str]] = [
    (r"\btab\.?\b|\btablet\b|\btablets\b", "tablet"),
    (r"\bcap\.?\b|\bcaps\b|\bcapsule\b|\bcapsules\b", "capsule"),
    (r"\bsyp\.?\b|\bsyr\.?\b|\bsyrup\b", "syrup"),
    (r"\binj\.?\b|\binjection\b", "injection"),
    (r"\boint\.?\b|\bointment\b", "ointment"),
    (r"\bcream\b", "cream"),
    (r"\bdrop\b|\bdrops\b", "drops"),
    (r"\bsusp\.?\b|\bsuspension\b", "suspension"),
    (r"\binhaler\b|\bpuff\b|\bpuffs\b", "inhaler"),
]

FREQUENCY_PATTERNS: List[str] = [
    r"\bOD\b", r"\bBD\b", r"\bTID\b", r"\bQID\b", r"\bHS\b", r"\bSOS\b", r"\bSTAT\b",
    r"\bQ\d+H\b", r"\bonce\s+daily\b", r"\btwice\s+daily\b", r"\bthrice\s+daily\b",
    r"\bonce\s+weekly\b", r"\bevery\s+\d+\s*hours?\b", r"\bbefore\s+meals?\b",
    r"\bafter\s+meals?\b", r"\bat\s+bedtime\b",
]

INSTRUCTION_CUES = {
    "take", "apply", "inject", "inhale", "use", "for", "x", "if", "prn", "before", "after", "at"
}

STRENGTH_RE = re.compile(
    r"\b\d+(?:\.\d+)?\s*(?:mg|mcg|g|kg|ml|iu|units|%)(?:\s*/\s*\d+(?:\.\d+)?\s*(?:ml|g))?\b",
    re.IGNORECASE,
)
DURATION_RE = re.compile(
    r"(?:\bfor\b|\bx\b)?\s*\d+\s*(?:day|days|week|weeks|month|months|hour|hours)\b",
    re.IGNORECASE,
)
DOSAGE_QUANTITY_RE = re.compile(
    r"\b(?:half|quarter|one|two|three|\d+(?:/\d+)?(?:\.\d+)?)\s*(?:tab(?:let)?s?|caps?(?:ule)?s?|ml|drops?|puffs?|sachets?|spoon(?:ful)?s?)\b",
    re.IGNORECASE,
)
DOSAGE_SCHEDULE_RE = re.compile(r"\b\d-\d-\d\b")


@dataclass
class SpanValue:
    start: int
    end: int
    value: str


@dataclass
class ParsedPrescription:
    raw_text: str
    medicine_name: str = ""
    form: str = ""
    strength: str = ""
    dosage: str = ""
    frequency: str = ""
    duration: str = ""
    notes: str = ""

    def to_dict(self) -> Dict[str, str]:
        return {
            "raw_text": self.raw_text,
            "medicine_name": self.medicine_name,
            "form": self.form,
            "strength": self.strength,
            "dosage": self.dosage,
            "frequency": self.frequency,
            "duration": self.duration,
            "notes": self.notes,
        }


def normalize_text(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def first_match(pattern: re.Pattern[str], text: str) -> Optional[SpanValue]:
    m = pattern.search(text)
    if not m:
        return None
    return SpanValue(m.start(), m.end(), m.group(0).strip())


def find_form(text: str) -> Optional[SpanValue]:
    for pat, normalized in FORM_ALIASES:
        m = re.search(pat, text, flags=re.IGNORECASE)
        if m:
            return SpanValue(m.start(), m.end(), normalized)
    return None


def find_frequency(text: str) -> Optional[SpanValue]:
    hits: List[SpanValue] = []
    for pat in FREQUENCY_PATTERNS:
        for m in re.finditer(pat, text, flags=re.IGNORECASE):
            val = m.group(0).strip()
            if val.upper() in {"OD", "BD", "TID", "QID", "HS", "SOS", "STAT"}:
                val = val.upper()
            hits.append(SpanValue(m.start(), m.end(), val))
    if not hits:
        return None
    hits.sort(key=lambda h: h.start)
    # Merge up to 2 unique frequency chunks for cases like "OD after meals"
    values: List[str] = []
    start = hits[0].start
    end = hits[0].end
    for hit in hits:
        if hit.value not in values:
            values.append(hit.value)
        end = max(end, hit.end)
        if len(values) == 2:
            break
    return SpanValue(start, end, ", ".join(values))


def find_dosage(text: str) -> Optional[SpanValue]:
    m1 = first_match(DOSAGE_QUANTITY_RE, text)
    m2 = first_match(DOSAGE_SCHEDULE_RE, text)
    if m1 and m2:
        return m1 if m1.start < m2.start else m2
    return m1 or m2


def strip_leading_form_tokens(text: str) -> str:
    return re.sub(
        r"^(?:rx[:\-]?\s*)?(?:tab\.?|tablet|cap\.?|capsule|inj\.?|injection|syp\.?|syr\.?|syrup|oint\.?|ointment)\s+",
        "",
        text,
        flags=re.IGNORECASE,
    )


def extract_medicine_name(text: str) -> str:
    candidate = strip_leading_form_tokens(text)
    tokens = candidate.split()
    if not tokens:
        return ""

    selected: List[str] = []
    for tok in tokens:
        low = tok.lower().strip(".,;:()[]{}?!")
        if not low:
            continue
        if low in INSTRUCTION_CUES:
            break
        if re.match(r"^\d", low):  # starts with number => likely strength/duration
            break
        if re.fullmatch(r"(od|bd|tid|qid|hs|sos|stat)", low):
            break
        selected.append(tok.strip(".,;:()[]{}?!"))
        if len(selected) >= 4:
            break

    # fallback: preserve first alpha token if empty
    if not selected:
        m = re.search(r"[A-Za-z][A-Za-z0-9+\-/]*", candidate)
        return m.group(0) if m else ""

    return " ".join(selected)


def build_mask(length: int, spans: Iterable[Optional[SpanValue]]) -> List[bool]:
    mask = [False] * length
    for sp in spans:
        if not sp:
            continue
        for i in range(max(0, sp.start), min(length, sp.end)):
            mask[i] = True
    return mask


def extract_notes(text: str, spans: Iterable[Optional[SpanValue]], medicine_name: str) -> str:
    mask = build_mask(len(text), spans)

    # Also mask the medicine_name text where present
    if medicine_name:
        for m in re.finditer(re.escape(medicine_name), text, flags=re.IGNORECASE):
            for i in range(m.start(), m.end()):
                mask[i] = True

    leftovers = "".join(ch if not mask[i] else " " for i, ch in enumerate(text))
    leftovers = re.sub(r"\b(?:tab\.?|tablet|cap\.?|capsule|syp\.?|syrup|inj\.?|injection|oint\.?|ointment|for)\b", " ", leftovers, flags=re.IGNORECASE)
    leftovers = re.sub(r"\s+", " ", leftovers).strip(" ,.-?")
    return leftovers


def parse_prescription(raw_text: str) -> Dict[str, str]:
    text = normalize_text(str(raw_text))

    form = find_form(text)
    strength = first_match(STRENGTH_RE, text)
    dosage = find_dosage(text)
    frequency = find_frequency(text)
    duration = first_match(DURATION_RE, text)

    medicine_name = extract_medicine_name(text)
    notes = extract_notes(text, [form, strength, dosage, frequency, duration], medicine_name)

    duration_value = ""
    if duration:
        duration_value = re.sub(r"^\s*(?:for|x)\s*", "", duration.value, flags=re.IGNORECASE).strip()
        duration_value = re.sub(r"(\d)(day|days|week|weeks|month|months|hour|hours)\b", r"\1 \2", duration_value, flags=re.IGNORECASE)

    parsed = ParsedPrescription(
        raw_text=text,
        medicine_name=medicine_name,
        form=form.value if form else "",
        strength=strength.value if strength else "",
        dosage=dosage.value if dosage else "",
        frequency=frequency.value if frequency else "",
        duration=duration_value,
        notes=notes,
    )
    return parsed.to_dict()


def _collect_raw_texts(obj: Any) -> List[str]:
    """Recursively collect raw text strings from different JSON structures."""
    results: List[str] = []

    if isinstance(obj, str):
        results.append(obj)
        return results

    if isinstance(obj, dict):
        if "raw_text" in obj and isinstance(obj["raw_text"], (str, int, float)):
            results.append(str(obj["raw_text"]))
        else:
            for val in obj.values():
                results.extend(_collect_raw_texts(val))
        return results

    if isinstance(obj, list):
        for item in obj:
            results.extend(_collect_raw_texts(item))
        return results

    return results


def load_records(input_path: Path) -> List[str]:
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    data = json.loads(input_path.read_text(encoding="utf-8"))
    records = [normalize_text(t) for t in _collect_raw_texts(data) if str(t).strip()]

    if not records:
        raise ValueError(
            "No prescription text found. Expected at least one raw text string in JSON (e.g., {'raw_text': '...'})."
        )
    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract structured data from raw prescription text")
    parser.add_argument("--input", default="prescription_raw_text_only.json", type=Path, help="Path to input JSON")
    parser.add_argument("--output", default="prescription_structured_output.json", type=Path, help="Path to output JSON")
    args = parser.parse_args()

    records = load_records(args.input)
    parsed = [parse_prescription(raw) for raw in records]

    args.output.write_text(json.dumps(parsed, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Processed {len(parsed)} records from {args.input} -> {args.output}")


if __name__ == "__main__":
    main()
