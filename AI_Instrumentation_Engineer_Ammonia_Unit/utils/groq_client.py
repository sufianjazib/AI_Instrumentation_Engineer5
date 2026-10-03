import os

def ask_groq(prompt: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return (
            "Groq API key not configured. The deterministic multi-agent "
            "diagnostic engine is still running. Add GROQ_API_KEY in "
            "Streamlit Cloud Secrets to enable LLM reasoning."
        )

    try:
        from groq import Groq

        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a concise industrial instrumentation "
                        "engineering assistant for a virtual ammonia-unit "
                        "training simulator."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=700,
        )
        return response.choices[0].message.content

    except Exception as exc:
        return f"Groq call failed; deterministic diagnosis remains available. Error: {exc}"
