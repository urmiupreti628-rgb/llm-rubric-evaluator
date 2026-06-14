"""Tests for rubric scoring logic."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from evaluate import evaluate_rows, score_label, weighted_score  # noqa: E402


class RubricScoringTest(unittest.TestCase):
    def test_weighted_score_uses_expected_weights(self) -> None:
        row = {"accuracy": "5", "relevance": "4", "clarity": "3", "safety": "2"}
        self.assertEqual(weighted_score(row), 3.9)

    def test_score_label_thresholds(self) -> None:
        self.assertEqual(score_label(4.8), "excellent")
        self.assertEqual(score_label(4.0), "good")
        self.assertEqual(score_label(3.2), "needs_review")
        self.assertEqual(score_label(2.9), "fail")

    def test_evaluate_rows_adds_score_and_label(self) -> None:
        rows = [
            {
                "id": "demo",
                "prompt": "What is PCR?",
                "response": "PCR copies DNA.",
                "accuracy": "5",
                "relevance": "5",
                "clarity": "4",
                "safety": "5",
                "notes": "Good.",
            }
        ]
        evaluated = evaluate_rows(rows)
        self.assertEqual(evaluated[0]["weighted_score"], "4.80")
        self.assertEqual(evaluated[0]["label"], "excellent")


if __name__ == "__main__":
    unittest.main()

