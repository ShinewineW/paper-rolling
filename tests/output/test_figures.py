from __future__ import annotations

from pathlib import Path

from scripts.output.figures import extract_figures, is_architecture_caption


def test_extract_figures_never_uses_an_image_ref_as_caption(tmp_path: Path) -> None:
    """Consecutive grid images (no caption between) must not grab the next image
    ref as their caption — they share the group caption that follows."""
    md = tmp_path / "p.md"
    md.write_text(
        "![](images/a.jpg)\n\n"
        "![](images/b.jpg)\n\n"
        "Figure 3: a grid of qualitative results.\n\n"
        "![](images/c.jpg)\n\n"
        "Figure 4: the model architecture overview.\n",
        encoding="utf-8",
    )
    figs = extract_figures(md)
    assert [f.ref for f in figs] == ["images/a.jpg", "images/b.jpg", "images/c.jpg"]
    assert all("![](" not in f.caption for f in figs)  # never an image-ref caption
    assert figs[0].caption.startswith("Figure 3")  # grid image gets the group caption
    assert is_architecture_caption(figs[2].caption)  # architecture figure detected


def test_is_architecture_caption() -> None:
    assert is_architecture_caption("Figure 2: overall architecture of our model")
    assert is_architecture_caption("图 1:整体框架")
    assert not is_architecture_caption("Figure 5: qualitative results on the test set")
