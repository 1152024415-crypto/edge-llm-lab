import json

from edge_llm_lab.phase1.prompts import load_prompt_set


def test_load_prompt_set_requires_core_baseline_fields(tmp_path):
    prompt_file = tmp_path / "prompts.json"
    prompt_file.write_text(
        json.dumps(
            {
                "name": "baseline",
                "prompts": [
                    {
                        "id": "zh-short",
                        "category": "chinese",
                        "text": "用三句话解释端侧 LLM 部署。",
                        "max_new_tokens": 64,
                        "expected_format": "plain_text",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    prompt_set = load_prompt_set(prompt_file)

    assert prompt_set.name == "baseline"
    assert prompt_set.prompts[0].id == "zh-short"
    assert prompt_set.prompts[0].max_new_tokens == 64
    assert prompt_set.prompts[0].expected_format == "plain_text"


def test_load_prompt_set_rejects_empty_prompt_list(tmp_path):
    prompt_file = tmp_path / "prompts.json"
    prompt_file.write_text('{"name":"baseline","prompts":[]}', encoding="utf-8")

    try:
        load_prompt_set(prompt_file)
    except ValueError as exc:
        assert "at least one prompt" in str(exc)
    else:
        raise AssertionError("expected ValueError")
