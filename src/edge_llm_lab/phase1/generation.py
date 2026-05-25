from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from edge_llm_lab.phase1.prompts import PromptSet
from edge_llm_lab.phase1.quality import evaluate_output_quality


def run_generation_pipeline(
    *,
    model_path: Path,
    prompt_set: PromptSet,
    device: str,
    temperature: float | None,
    top_p: float | None,
) -> dict[str, object]:
    import openvino as ov
    import openvino_genai as ov_genai

    load_start = time.perf_counter()
    pipe = ov_genai.LLMPipeline(str(model_path), device)
    load_seconds = time.perf_counter() - load_start

    prompt_results: list[dict[str, object]] = []
    for prompt in prompt_set.prompts:
        generation_start = time.perf_counter()
        raw_result = pipe.generate(
            prompt.text,
            **build_generation_kwargs(
                max_new_tokens=prompt.max_new_tokens,
                temperature=temperature,
                top_p=top_p,
            ),
        )
        generation_seconds = time.perf_counter() - generation_start
        output_text = normalize_generation_result(raw_result)
        quality = evaluate_output_quality(
            output_text,
            expected_format=prompt.expected_format,
        )
        prompt_results.append(
            {
                "id": prompt.id,
                "category": prompt.category,
                "prompt": prompt.text,
                "max_new_tokens": prompt.max_new_tokens,
                "expected_format": prompt.expected_format,
                "output": output_text,
                "generation_seconds": generation_seconds,
                "quality": {
                    "passed": quality.passed,
                    "failures": quality.failures,
                },
            }
        )

    return {
        "schema_version": 1,
        "model_path": str(model_path),
        "device": device,
        "openvino_version": getattr(ov, "__version__", "unknown"),
        "generation_config": {
            "decode_method": "greedy" if temperature is None and top_p is None else "sampling",
            "temperature": temperature,
            "top_p": top_p,
        },
        "load_seconds": load_seconds,
        "prompts": prompt_results,
    }


def normalize_generation_result(result: Any) -> str:
    if isinstance(result, str):
        return result
    if hasattr(result, "texts"):
        texts = getattr(result, "texts")
        if isinstance(texts, list) and texts:
            return str(texts[0])
    return str(result)


def build_generation_kwargs(
    *,
    max_new_tokens: int,
    temperature: float | None,
    top_p: float | None,
) -> dict[str, object]:
    kwargs: dict[str, object] = {"max_new_tokens": max_new_tokens}
    if temperature is not None:
        if temperature <= 0:
            raise ValueError("temperature must be positive when sampling is enabled")
        kwargs["temperature"] = temperature
    if top_p is not None:
        kwargs["top_p"] = top_p
    return kwargs


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
