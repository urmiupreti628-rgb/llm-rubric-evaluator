# LLM Rubric Evaluator

Rubric-based evaluator for short LLM prompt-response pairs.

## Project Overview

This project shows how to evaluate language model outputs with a repeatable scoring process. It uses a four-part rubric covering accuracy, relevance, clarity, and safety. The project includes sample prompt-response rows, human-assigned scores, a scoring script, and tests for the scoring logic.

This is intentionally simple and transparent. It is designed to demonstrate AI evaluation thinking, not to replace expert review or enterprise evaluation platforms.

## Repository Contents

```text
data/evaluation_rows.csv      Sample prompt-response evaluations
scripts/evaluate.py           Weighted scoring and reporting script
tests/test_scoring.py         Unit tests for scoring logic
RUBRIC.md                     Detailed scoring rubric
requirements.txt              Dependency note
```

## Evaluation Method

Each response is scored from 1 to 5 on four dimensions:

| Dimension | Weight |
| --- | ---: |
| Accuracy | 40% |
| Relevance | 25% |
| Clarity | 20% |
| Safety | 15% |

The weighted score is calculated as:

```text
accuracy*0.40 + relevance*0.25 + clarity*0.20 + safety*0.15
```

The script then assigns a label:

| Score Range | Label |
| ---: | --- |
| 4.50-5.00 | Excellent |
| 3.75-4.49 | Good |
| 3.00-3.74 | Needs review |
| 1.00-2.99 | Fail |

## How to Run

```bash
python scripts/evaluate.py
python -m unittest discover tests
```

The script writes:

```text
reports/scored_outputs.csv
reports/evaluation_summary.json
```

## Current Results

The sample dataset contains 15 evaluated prompt-response rows. Most examples are high-quality microbiology education answers, while one deliberately weak response is included to show how the rubric handles incorrect or unsafe content.

## Why This Project Matters

LLM evaluation work often requires clear rubrics, consistent scoring, and readable reporting. This project demonstrates:

- Rubric design
- Human evaluation data structure
- Weighted score calculation
- Error checking for score fields
- Summary reporting
- Unit testing for evaluation logic

## Limitations

The sample set is small and manually scored. A production-grade evaluation would include multiple annotators, inter-annotator agreement, larger prompt coverage, blind review, and model/version metadata.

