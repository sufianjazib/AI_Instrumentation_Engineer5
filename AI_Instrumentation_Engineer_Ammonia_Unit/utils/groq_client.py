import os

def _get_secret(name: str, default=None):
    # Streamlit Cloud stores secrets in st.secrets rather than the OS
    # environment. Environment variables are still supported for local use.
    value = os.getenv(name)
    if value:
        return value

    try:
        import streamlit as st
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        pass

    return default


def ask_groq(prompt: str) -> str:
    api_key = _get_secret("GROQ_API_KEY")
    model = _get_secret("GROQ_MODEL", "llama-3.3-70b-versatile")

    if not api_key:
        return (
            "Groq API key is not configured. The deterministic multi-agent "
            "diagnostic engine is still running. Add GROQ_API_KEY to "
            "Streamlit Cloud Secrets."
        )

    try:
        from groq import Groq

        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an industrial instrumentation engineering "
                        "assistant for a virtual ammonia-unit training simulator. "
                        "Be concise, evidence-based and safety-conscious."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=700,
        )
        return response.choices[0].message.content

    except Exception as exc:
        return (
            "Groq call failed; deterministic diagnosis remains available. "
            f"Error: {exc}"
        )
