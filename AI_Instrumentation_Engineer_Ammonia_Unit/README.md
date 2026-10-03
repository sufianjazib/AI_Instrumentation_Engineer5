# AI Instrumentation Engineer — Ammonia Unit

A Streamlit-based multi-agent engineering demonstrator for detecting abnormal
instrument behavior, identifying probable instrumentation faults, and
generating structured troubleshooting guidance for a virtual ammonia unit.

## Features

- Virtual ammonia-unit process
- PT, TT, FT, LT and ammonia analyzer tags
- Fault injection
- Instrument health dashboard
- Five-agent diagnostic architecture
- Groq LLM integration
- Technician-oriented troubleshooting
- Safety review layer
- Streamlit Cloud deployment

## Architecture

Monitoring Agent
→ Process Agent
→ Diagnostics Agent
→ Troubleshooting Agent
→ Safety Agent
→ Groq LLM

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

For local Groq use, create `.streamlit/secrets.toml` from
`.streamlit/secrets.toml.example`.

## Streamlit Cloud

1. Create a GitHub repository.
2. Upload this project.
3. Create a Streamlit Cloud app from the repository.
4. Main file: `app.py`.
5. Add these Secrets in the Streamlit Cloud settings:

```toml
GROQ_API_KEY = "gsk_your_key_here"
GROQ_MODEL = "openai/gpt-oss-120b"
```

6. Deploy.

## Important

This is a training/demo simulator. It is not a real plant control system,
SIS, safety system, or replacement for qualified engineering judgement and
site procedures. Do not use AI output to bypass interlocks, alarms, permits,
isolation/LOTO, or other plant safeguards.
