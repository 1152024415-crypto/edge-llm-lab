from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PromptCase:
    id: str
    category: str
    text: str
    max_new_tokens: int
    expected_format: str


@dataclass(frozen=True)
class PromptSet:
    name: str
    prompts: list[PromptCase]


def load_prompt_set(path: Path) -> PromptSet:
    data = json.loads(path.read_text(encoding="utf-8"))
    name = require_text(data, "name")
    raw_prompts = data.get("prompts")
    if not isinstance(raw_prompts, list) or not raw_prompts:
        raise ValueError("prompt set must contain at least one prompt")

    prompts: list[PromptCase] = []
    for index, item in enumerate(raw_prompts):
        if not isinstance(item, dict):
            raise ValueError(f"prompt {index} must be an object")
        prompts.append(
            PromptCase(
                id=require_text(item, "id"),
                category=require_text(item, "category"),
                text=require_text(item, "text"),
                max_new_tokens=require_positive_int(item, "max_new_tokens"),
                expected_format=str(item.get("expected_format", "plain_text")),
            )
        )
    return PromptSet(name=name, prompts=prompts)


def require_text(data: dict[str, object], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a non-empty string")
    return value


def require_positive_int(data: dict[str, object], key: str) -> int:
    value = data.get(key)
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{key} must be a positive integer")
    return value
