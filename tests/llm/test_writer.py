from scripts.llm.writer import _section_prompt


def test_section_prompt_prior_failure_injected():
    assert "PSNR(21.14)" in _section_prompt("t", "f", "s", prior_failure="上次:PSNR(21.14)在散文里")


def test_section_prompt_default_unchanged():
    assert "上一稿" not in _section_prompt("t", "f", "s")
