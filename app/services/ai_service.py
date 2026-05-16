import ollama

import json

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

def generate_flashcards(
    content: str
):
    truncated_content = content[:2500]

    response = ollama.chat(
        model="mistral",
        messages=[
            {
                "role": "system",
                "content": (
                    "Generate 5 educational flashcards "
                    "in JSON format. "
                    "Return ONLY valid JSON."
                )
            },
            {
                "role": "user",
                "content": f"""
Generate flashcards from this material.

Return this format ONLY:

[
  {{
    "question": "...",
    "answer": "..."
  }}
]

Material:

{truncated_content}
"""
            }
        ]
    )

    content_response = (
        response["message"]["content"]
    )

    try:
        flashcards = json.loads(
            content_response
        )

        return flashcards

    except:
        return []