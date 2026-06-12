from scripts.paths import ara_is_nonempty


def test_nonempty_ara_dir_true(tmp_path):
    ara = tmp_path / "ara"
    (ara / "logic").mkdir(parents=True)
    (ara / "PAPER.md").write_text("x", encoding="utf-8")
    assert ara_is_nonempty(ara) is True


def test_empty_ara_dir_false(tmp_path):
    ara = tmp_path / "ara"
    ara.mkdir()
    assert ara_is_nonempty(ara) is False


def test_missing_ara_dir_false(tmp_path):
    assert ara_is_nonempty(tmp_path / "ara") is False


def test_dir_with_only_empty_subdir_false(tmp_path):
    ara = tmp_path / "ara"
    (ara / "logic").mkdir(parents=True)  # subdir but no file
    assert ara_is_nonempty(ara) is False
