# Repository Guidelines

## Project Structure & Module Organization
- Root modules: `main.py` (entry), `handlers.py` (Telegram handlers), `auth.py` (area access), `bot_config.py` (YAML config loader).
- Integrations: `providers/` (tuya, lg_thinq, smartthings, others).
- Configuration: `config/bot.yaml` (copy from `config/bot.example.yaml`).
- Secrets: `.env` (copy from `.env.example`).
- Legacy prototypes: `LG_Thinq.py`, `Samsung Things.py` (reference for future provider wiring).

## Build, Test, and Development Commands
- Create venv and install: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
- Configure: `cp .env.example .env && cp config/bot.example.yaml config/bot.yaml`.
- Run locally: `python main.py`.
- Lint/format (optional): if you add tools, prefer `ruff`, `black`, `isort`; keep configs minimal.

## Coding Style & Naming Conventions
- Python 3.9+; PEP 8; 4‑space indent; UTF‑8.
- Type hints required; short doctrings for public functions.
- Naming: modules `snake_case.py`, functions/vars `snake_case`, classes `PascalCase`, constants `UPPER_SNAKE`.
- Handlers: async functions in `handlers.py`; register in `main.py` with `CommandHandler`/`MessageHandler`.
- Access control: protect area‑scoped commands with `auth.guard(area_arg_index=0, command_name="...")`.

## Testing Guidelines
- No test suite yet. If adding tests:
  - Framework: `pytest` under `tests/` (mirror module paths).
  - Use sample config: `config/bot.example.yaml` with temporary IDs.
  - Mock Telegram updates and provider calls.
  - Run: `pytest -q`.

## Commit & Pull Request Guidelines
- Use Conventional Commits style: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`.
- Commits: imperative mood, ≤50 char subject; explain why in body when nontrivial.
- PRs: clear description, linked issues, before/after behavior, run steps; include config/README updates when relevant.

## Security & Configuration Tips
- Never commit real tokens/IDs; keep them in `.env` and local `config/bot.yaml`.
- Restrict `admins` and `areas.*.members` to exact Telegram user IDs.
- Limit `areas.*.commands` to the minimum required (e.g., `open_door` only for `office`).
