#!/usr/bin/env python3
"""Simple quality summary for extracted prescription fields."""

from __future__ import annotations

import json
from pathlib import Path

IN_PATH = Path("prescription_structured_output.json")
OUT_PATH = Path("evaluation_summary.md")


def main() -> None:
    rows = json.loads(IN_PATH.read_text(encoding="utf-8"))
    total = len(rows)
    required = ["medicine_name", "form", "strength", "dosage", "frequency", "duration", "notes"]

    non_empty_rates = {}
    for field in required:
        non_empty = sum(1 for r in rows if str(r.get(field, "")).strip())
        non_empty_rates[field] = (non_empty, total)

    likely_failures = [
        r for r in rows if (not r.get("medicine_name")) or sum(bool(str(r.get(f, "")).strip()) for f in required) <= 2
    ]

    lines = [
        "# Evaluation Summary",
        "",
        f"- Total records: **{total}**",
        "- Non-empty extraction coverage:",
    ]
    for field, (count, denom) in non_empty_rates.items():
        pct = 100 * count / denom if denom else 0
        lines.append(f"  - `{field}`: {count}/{denom} ({pct:.1f}%)")

    lines += ["", "## Correct-looking examples", ""]
    for row in rows[:3]:
        lines.append(f"- Raw: `{row['raw_text']}`")
        lines.append(
            f"  - Extracted: medicine=`{row['medicine_name']}`, dosage=`{row['dosage']}`, freq=`{row['frequency']}`, duration=`{row['duration']}`"
        )

    lines += ["", "## Likely failure cases", ""]
    if not likely_failures:
        lines.append("- No obvious failures by heuristic checks.")
    else:
        for row in likely_failures[:5]:
            lines.append(f"- Raw: `{row['raw_text']}`")
            lines.append(f"  - Output: `{json.dumps(row, ensure_ascii=False)}`")

    lines += [
        "",
        "## Notes on tradeoffs",
        "",
        "- Regex+rules are transparent and fast but fragile on unseen shorthand.",
        "- For production, add supervised sequence labeling or weakly supervised patterns over annotated data.",
    ]

    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
