# Deep Research Using OpenAI Agent SDK

A Gradio app that runs a multi-agent research workflow:
- plan web searches
- execute searches
- write a detailed markdown report
- send the report by email

## Project Structure

- `app.py` - Gradio UI entrypoint
- `src/research_manager.py` - workflow orchestration
- `src/agents/` - planner, search, writer, and email agents
- `src/config.py` - environment-backed settings loader
- `src/prompts.py` - centralized prompt/instruction constants

## Required Environment Variables

Create a `.env` file in the project root with at least:

```env
OPENAI_API_KEY=your_openai_key
SENDGRID_API_KEY=your_sendgrid_key
SENDER_EMAIL=verified_sender@example.com
RECIPIENT_EMAIL=recipient@example.com
```

Optional:

```env
PLANNER_SEARCH_COUNT=5
```

## Setup and Run (Using `uv`)

1. Install uv (if needed):
   - [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Create and sync the environment from `pyproject.toml`:

```bash
uv sync
```

3. Run the app:

```bash
uv run app.py
```

The UI opens in your browser (`app.py` launches Gradio with `inbrowser=True`).

## Setup and Run (Using `pip`)

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Alternatively, install directly from `pyproject.toml`:

```bash
pip install .
```

3. Run the app:

```bash
python app.py
```

## Notes

- If email sending fails, verify `SENDGRID_API_KEY`, `SENDER_EMAIL`, and recipient settings.
- Keep secrets in `.env` only; do not commit credentials to git.
