import json

from scripts.ingest.contract import (
    MdContract,
    count_equation_blocks,
    sha256_bytes,
    write_contract,
)


def test_sha256_bytes_is_hex_of_known_input():
    # sha256("") is a well-known constant
    assert sha256_bytes(b"") == ("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")


def test_count_equation_blocks_counts_paired_display_fences():
    md = "intro\n$$a = b$$\nmiddle\n$$\nc = d\n$$\nend\n"
    assert count_equation_blocks(md) == 2


def test_count_equation_blocks_ignores_inline_and_unpaired():
    # inline $x$ must not count; a lone unpaired $$ must not count
    md = "inline $x = y$ text\n$$ paired = 1 $$\nstray $$ dangling\n"
    assert count_equation_blocks(md) == 1


def test_mdcontract_to_dict_has_exact_six_fields():
    c = MdContract(
        source_pdf_sha256="abc",
        converter="pandoc",
        converter_version="3.1.2",
        md_sha256="def",
        image_count=4,
        equation_block_count=7,
    )
    d = c.to_dict()
    assert set(d) == {
        "source_pdf_sha256",
        "converter",
        "converter_version",
        "md_sha256",
        "image_count",
        "equation_block_count",
    }
    assert d["image_count"] == 4
    assert d["equation_block_count"] == 7


def test_write_contract_emits_json_file(tmp_path):
    c = MdContract(
        source_pdf_sha256=None,
        converter="pandoc",
        converter_version="3.1.2",
        md_sha256="deadbeef",
        image_count=0,
        equation_block_count=0,
    )
    out = tmp_path / ".md_contract.json"
    write_contract(c, out)
    loaded = json.loads(out.read_text())
    # Tier-1 (no PDF) → source_pdf_sha256 is null, serialized as JSON null
    assert loaded["source_pdf_sha256"] is None
    assert loaded["converter"] == "pandoc"
    assert loaded["md_sha256"] == "deadbeef"
