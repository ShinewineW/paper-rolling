# Repository Guidelines

## Project Structure & Module Organization

`paper-rolling` is a Python research-paper processing workspace. Core engine code lives in `.claude/skills/paper-landscape/scripts/`, with major packages for `discovery`, `ingest`, `llm`, `ledger`, `output`, and `audit`. Tests mirror those areas under `tests/`. Project docs live in `docs/`, especially `docs/INDEX.md`, `docs/guides/`, and `docs/adr/`. Runtime and product data are part of the repository: `corpus/`, `person_vault/`, `ai_package/`, `landscapes/`, `_ledger/`, and `config/`.

## Build, Test, and Development Commands

- `uv sync --group dev`: create/update the development environment.
- `uv run pytest`: run the full executable test suite.
- `uv run pytest tests/output/test_naming.py`: run a focused test file.
- `uv run ruff check .`: run repo-wide linting.
- `PYTHONPATH=.claude/skills/paper-landscape uv run python -m scripts.preflight`: verify runtime dependencies such as `pandoc` and MinerU before campaign work.

There is no separate build target; passing pytest plus ruff is the normal validation gate.

## Coding Style & Naming Conventions

Use Python 3.11+ conventions with 4-space indentation. Ruff is configured for 100-character lines and rules `E`, `F`, `I`, `UP`, and `B`; keep imports sorted and avoid broad exception handling. Prefer deterministic, dependency-injected functions in engine code. Use clear snake_case module, function, and variable names. Tests should be named `test_*.py` and should describe behavior rather than implementation detail.

## Testing Guidelines

Add or update focused tests for any behavior change. Place tests near the matching subsystem, for example `tests/discovery/`, `tests/ingest/`, `tests/output/`, or `tests/audit/`. Use fake seams/adapters for LLM-backed or I/O-heavy behavior so tests stay deterministic. For command-line helpers, include CLI-level coverage where practical.

## Commit & Pull Request Guidelines

Recent history uses short conventional-style commits such as `fix(audit): ...`, `docs: ...`, and `chore: ...`. Follow that pattern: start with a type, add a scope when useful, and keep the subject concrete. Pull requests should describe the behavioral change, list validation commands run, and call out any changes to tracked product directories such as `person_vault/`, `ai_package/`, `_ledger/`, or `landscapes/`.

## Security & Configuration Tips

Never commit secrets. `.env`, caches, PDFs, MinerU intermediates, and machine-local Claude settings are ignored. Do not add broad ignore rules for tracked knowledge products; this repository intentionally tracks generated reports, ledgers, configs, and curated assets.
