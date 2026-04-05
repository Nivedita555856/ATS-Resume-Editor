# Evaluation Summary

- Total records: **10**
- Non-empty extraction coverage:
  - `medicine_name`: 10/10 (100.0%)
  - `form`: 9/10 (90.0%)
  - `strength`: 7/10 (70.0%)
  - `dosage`: 4/10 (40.0%)
  - `frequency`: 8/10 (80.0%)
  - `duration`: 8/10 (80.0%)
  - `notes`: 6/10 (60.0%)

## Correct-looking examples

- Raw: `Tab. Amitriptyline 25 mg 1 tablet OD for 5 days at bedtime`
  - Extracted: medicine=`Amitriptyline`, dosage=`1 tablet`, freq=`OD, at bedtime`, duration=`5 days`
- Raw: `Cap Azithromycin 500mg 1 cap OD x 3 days after meals`
  - Extracted: medicine=`Azithromycin`, dosage=`1 cap`, freq=`OD, after meals`, duration=`3 days`
- Raw: `Syp Coughnil 5 ml BD for 7 days`
  - Extracted: medicine=`Coughnil`, dosage=`5 ml`, freq=`BD`, duration=`7 days`

## Likely failure cases

- No obvious failures by heuristic checks.

## Notes on tradeoffs

- Regex+rules are transparent and fast but fragile on unseen shorthand.
- For production, add supervised sequence labeling or weakly supervised patterns over annotated data.
