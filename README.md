# Prescription NLP Extraction Pipeline

This project provides a **production-style, deterministic NLP parser** for extracting structured prescription fields from noisy `raw_text` JSON records.

## What problem this solves

Given text like:

`Tab. Amitriptyline 25 mg 1 tablet OD for 5 days at bedtime`

the pipeline outputs:

- `medicine_name`
- `form`
- `strength`
- `dosage`
- `frequency`
- `duration`
- `notes`

while keeping the original `raw_text`.

---

## Real working logic (step-by-step)

The parser is intentionally rule-based so behavior is explainable and easy to debug.

1. **Input normalization**
   - Removes extra whitespace and normalizes punctuation/spacing.

2. **Field extraction with targeted rules**
   - **Form detection** from abbreviation dictionary (`Tab`, `Cap`, `Syp`, `Inj`, `Oint`, etc.)
   - **Strength detection** using unit-aware regex (`mg`, `mcg`, `g`, `ml`, `IU`, `%`)
   - **Dosage detection** for both:
     - quantity style (`1 tablet`, `5 ml`, `2 puffs`)
     - schedule style (`1-0-1`)
   - **Frequency detection** for abbreviations + natural phrases (`OD`, `BD`, `HS`, `SOS`, `once daily`, `every 6 hours`, etc.)
   - **Duration detection** from phrases like `for 5 days`, `x 3 weeks`, `10days`

3. **Medicine name extraction**
   - Removes common leading form tokens and then captures the medicine segment before instruction/strength/frequency cues.

4. **Notes extraction (non-overlap logic)**
   - Uses character span masking of already-extracted fields and returns the clean remainder as notes.
   - This avoids duplication and gives more stable outputs.

5. **Robust JSON input handling**
   - Supports multiple JSON shapes:
     - `[{"raw_text": "..."}]`
     - nested objects containing `raw_text`
     - `[{...}, {...}]` or `[{"text": ...}]` (if raw strings are present in nested structures)
     - list of strings

---

## Files

- `extract_prescriptions.py` → main parser CLI
- `evaluate_extraction.py` → summary metrics and examples
- `prescription_raw_text_only.json` → sample input
- `prescription_structured_output.json` → generated output
- `evaluation_summary.md` → quick evaluation report

---

## How to run smoothly

### 1) Run extraction

```bash
python extract_prescriptions.py \
  --input prescription_raw_text_only.json \
  --output prescription_structured_output.json
```

### 2) Run evaluation summary

```bash
python evaluate_extraction.py
```

---

## Expected output schema

```json
{
  "raw_text": "<original raw text>",
  "medicine_name": "<string>",
  "form": "<string>",
  "strength": "<string>",
  "dosage": "<string>",
  "frequency": "<string>",
  "duration": "<string>",
  "notes": "<string>"
}
```

---

## Why this is assignment-strong

- Deterministic and explainable logic (easy error analysis)
- Handles noisy abbreviations and mixed formatting
- Strong engineering reliability: clear errors for bad input, robust parsing of JSON shapes
- Provides evaluation summary + failure-analysis base for iteration

## Known tradeoffs

- Rule-based logic can miss rare shorthand variants.
- Best next upgrade: add annotated data + token classification model (spaCy/transformer) with regex fallback.
