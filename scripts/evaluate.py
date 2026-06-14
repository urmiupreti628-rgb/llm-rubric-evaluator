"""Evaluate prompt-response rows with a weighted rubric."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


WEIGHTS = {
    "accuracy": 0.40,
    "relevance": 0.25,
    "clarity": 0.20,
    "safety": 0.15,
}


def weighted_score(row: dict[str, str]) -> float:
    return round(sum(float(row[metric]) * weight for metric, weight in WEIGHTS.items()), 2)


def score_label(score: float) -> str:
    if score >= 4.50:
        return "excellent"
    if score >= 3.75:
        return "good"
    if score >= 3.00:
        return "needs_review"
    return "fail"


def validate_score(value: str, row_id: str, metric: str) -> int:
    try:
        score = int(value)
    except ValueError as exc:
        raise ValueError(f"{row_id}: {metric} must be an integer from 1 to 5") from exc
    if score < 1 or score > 5:
        raise ValueError(f"{row_id}: {metric} must be between 1 and 5")
    return score


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    required = {"id", "prompt", "response", "notes", *WEIGHTS.keys()}
    for row in rows:
        missing = required - set(row)
        if missing:
            raise ValueError(f"{row.get('id', '<unknown>')}: missing fields {sorted(missing)}")
        for metric in WEIGHTS:
            validate_score(row[metric], row["id"], metric)
    return rows


def evaluate_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    evaluated: list[dict[str, str]] = []
    for row in rows:
        score = weighted_score(row)
        evaluated.append({**row, "weighted_score": f"{score:.2f}", "label": score_label(score)})
    return evaluated


def summarize(rows: list[dict[str, str]]) -> dict:
    scores = [float(row["weighted_score"]) for row in rows]
    labels = Counter(row["label"] for row in rows)
    metric_averages = {
        metric: round(sum(int(row[metric]) for row in rows) / len(rows), 2)
        for metric in WEIGHTS
    }
    return {
        "row_count": len(rows),
        "average_weighted_score": round(sum(scores) / len(scores), 2),
        "min_weighted_score": min(scores),
        "max_weighted_score": max(scores),
        "label_distribution": dict(labels),
        "metric_averages": metric_averages,
    }


def write_scored_csv(rows: list[dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Score LLM responses with a rubric.")
    parser.add_argument("--input", default="data/evaluation_rows.csv", help="CSV with rubric scores.")
    parser.add_argument("--scored-output", default="reports/scored_outputs.csv", help="Scored CSV path.")
    parser.add_argument("--summary-output", default="reports/evaluation_summary.json", help="Summary JSON path.")
    args = parser.parse_args()

    rows = load_rows(Path(args.input))
    evaluated = evaluate_rows(rows)
    summary = summarize(evaluated)

    write_scored_csv(evaluated, Path(args.scored_output))
    summary_path = Path(args.summary_output)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

