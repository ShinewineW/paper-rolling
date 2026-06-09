import json
from pathlib import Path

from scripts.failure_scene import write_scene


def test_write_scene_self_contained(tmp_path: Path):
    staged = tmp_path / "staging"
    (staged / "ai" / "ara").mkdir(parents=True)
    (staged / "ai" / "ara" / "PAPER.md").write_text("ssot", encoding="utf-8")
    (staged / "person").mkdir(parents=True)
    (staged / "person" / "report.md").write_text("report", encoding="utf-8")
    content_list = tmp_path / "content_list.json"
    content_list.write_text("[]", encoding="utf-8")

    scene = write_scene(
        workspace=tmp_path,
        key="2026-06-09_Foo_1234.5678",
        ledger_key="1234.5678",
        failed_gate="最终门",
        findings=[
            {"severity": "hard", "target": "report.md", "observation": "PSNR(21.14) in prose"}
        ],
        engine_commit="19c24e3",
        candidate={"arxiv_id": "1234.5678", "title": "Foo", "doi": None},
        md_path=tmp_path / "corpus" / "x.md",
        content_list_path=content_list,
        analysis={"bundle": "stub"},
        staged_dir=staged,
    )
    assert (scene / "ai" / "ara" / "PAPER.md").read_text() == "ssot"
    assert (scene / "person" / "report.md").read_text() == "report"
    assert (scene / "content_list.json").read_text() == "[]"  # gitignored 产物拷入现场
    assert not staged.exists()
    m = json.loads((scene / "scene.json").read_text())
    assert m["ledger_key"] == "1234.5678"  # 复活回写原 ledger 行(审计 high)
    assert m["candidate"]["arxiv_id"] == "1234.5678"
    assert m["md_path"].endswith("x.md")
    assert m["analysis"] == {"bundle": "stub"}
    assert m["failed_gate"] == "最终门"
    assert len(m["attempts"]) == 1 and m["attempts"][0]["failed_gate"] == "最终门"  # 角度 4


def test_write_scene_appends_attempt_history(tmp_path: Path):
    """再失败追加而非覆盖：第二次 write_scene 后 attempts 应有 2 条（角度 4）。"""

    def _write(gate, obs):
        staged = tmp_path / f"st_{gate}"
        (staged / "ai" / "ara").mkdir(parents=True)
        return write_scene(
            workspace=tmp_path,
            key="k1",
            ledger_key="1234.5678",
            failed_gate=gate,
            findings=[{"severity": "hard", "target": "report.md", "observation": obs}],
            engine_commit="c1",
            candidate={"arxiv_id": "1234.5678", "title": "F", "doi": None},
            md_path=tmp_path / "x.md",
            content_list_path=None,
            analysis=None,
            staged_dir=staged,
        )

    _write("最终门", "first fail")
    scene = _write("最终门", "second fail after a fix")
    m = json.loads((scene / "scene.json").read_text())
    assert len(m["attempts"]) == 2
    assert m["attempts"][0]["findings"][0]["observation"] == "first fail"
    assert m["attempts"][1]["findings"][0]["observation"] == "second fail after a fix"


def test_write_scene_self_referential_content_list_survives_append(tmp_path: Path):
    """审计 R3 Finding 2:复活 append 历史时 content_list 源就在 scene 内,rmtree 不得自毁它。"""
    staged1 = tmp_path / "st1"
    (staged1 / "ai" / "ara").mkdir(parents=True)
    cl = tmp_path / "content_list.json"
    cl.write_text('[{"type":"equation"}]', encoding="utf-8")
    scene = write_scene(
        workspace=tmp_path,
        key="k1",
        ledger_key="1234.5678",
        failed_gate="最终门",
        findings=[{"severity": "hard", "target": "report.md", "observation": "f1"}],
        engine_commit="c1",
        candidate={"arxiv_id": "1234.5678", "title": "F", "doi": None},
        md_path=tmp_path / "x.md",
        content_list_path=cl,
        analysis=None,
        staged_dir=staged1,
    )
    assert (scene / "content_list.json").exists()
    # 第二次:content_list_path 指向现场内自身 → rmtree 前快照保护,内容必须存活。
    staged2 = tmp_path / "st2"
    (staged2 / "ai" / "ara").mkdir(parents=True)
    scene = write_scene(
        workspace=tmp_path,
        key="k1",
        ledger_key="1234.5678",
        failed_gate="最终门",
        findings=[{"severity": "hard", "target": "report.md", "observation": "f2"}],
        engine_commit="c2",
        candidate={"arxiv_id": "1234.5678", "title": "F", "doi": None},
        md_path=tmp_path / "x.md",
        content_list_path=scene / "content_list.json",  # 自指:源在 scene 内
        analysis=None,
        staged_dir=staged2,
    )
    assert (scene / "content_list.json").read_text() == '[{"type":"equation"}]'
    assert len(json.loads((scene / "scene.json").read_text())["attempts"]) == 2
