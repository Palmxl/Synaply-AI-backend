import ollama


def generate_summary(
    content: str
):
    truncated_content = content[:2500]

    response = ollama.chat(
        model="mistral",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI study assistant. "
                    "Generate concise educational summaries."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Summarize this study material:\n\n"
                    f"{truncated_content}"
                )
            }
        ]
    )

    return response["message"]["content"]