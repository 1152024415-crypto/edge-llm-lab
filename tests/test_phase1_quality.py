from edge_llm_lab.phase1.quality import evaluate_output_quality
from edge_llm_lab.phase1.generation import build_generation_kwargs


def test_evaluate_output_quality_passes_clear_output():
    result = evaluate_output_quality("端侧部署需要关注模型大小、延迟和功耗。")

    assert result.passed is True
    assert result.failures == []


def test_evaluate_output_quality_rejects_empty_and_repetition():
    empty = evaluate_output_quality("")
    repeated = evaluate_output_quality("token token token token token token token token")

    assert empty.passed is False
    assert "empty-output" in empty.failures
    assert repeated.passed is False
    assert "repetition-suspected" in repeated.failures


def test_evaluate_output_quality_can_require_strict_json_object():
    valid = evaluate_output_quality(
        '{"model_size":"small","latency":"low","quality":"stable"}',
        expected_format="json_object",
    )
    fenced = evaluate_output_quality(
        '```json\n{"model_size":"small"}\n```\nextra explanation',
        expected_format="json_object",
    )

    assert valid.passed is True
    assert fenced.passed is False
    assert "invalid-json-object" in fenced.failures


def test_build_generation_kwargs_omits_sampling_for_greedy_decode():
    kwargs = build_generation_kwargs(max_new_tokens=64, temperature=None, top_p=None)

    assert kwargs == {"max_new_tokens": 64}


def test_build_generation_kwargs_rejects_zero_temperature_sampling():
    try:
        build_generation_kwargs(max_new_tokens=64, temperature=0.0, top_p=1.0)
    except ValueError as exc:
        assert "temperature must be positive" in str(exc)
    else:
        raise AssertionError("expected ValueError")
