import ollama


def generate_summary(
    content: str
):
    truncated_content = content[:12000]

    response = ollama.chat(
        model="llama3",
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