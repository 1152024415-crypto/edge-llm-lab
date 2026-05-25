from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass(frozen=True)
class QualityResult:
    passed: bool
    failures: list[str]


def evaluate_output_quality(text: str, *, expected_format: str = "plain_text") -> QualityResult:
    failures: list[str] = []
    stripped = text.strip()
    if not stripped:
        failures.append("empty-output")
    if "\ufffd" in text:
        failures.append("replacement-character")
    if looks_repetitive(stripped):
        failures.append("repetition-suspected")
    if expected_format == "json_object" and not is_strict_json_object(stripped):
        failures.append("invalid-json-object")
    return QualityResult(passed=not failures, failures=failures)


def looks_repetitive(text: str) -> bool:
    words = text.split()
    if len(words) < 8:
        return False
    most_common_count = max(words.count(word) for word in set(words))
    return most_common_count / len(words) >= 0.5


def is_strict_json_object(text: str) -> bool:
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return False
    return isinstance(parsed, dict)
