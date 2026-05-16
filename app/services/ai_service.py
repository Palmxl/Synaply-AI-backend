import json

import ollama

from app.services.vector_service import (
    search_similar_chunks
)


MODEL_NAME = "phi3"


def generate_summary(
    content: str
):
    truncated_content = content[:2500]

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI study assistant.\n"
                    "Generate concise and easy-to-understand educational summaries.\n"
                    "Avoid repetition.\n"
                    "Use short paragraphs.\n"
                    "Keep the response focused."
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
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI study assistant.\n"
                    "Generate educational flashcards.\n"
                    "Return ONLY valid JSON.\n"
                    "Do not add explanations or markdown."
                )
            },
            {
                "role": "user",
                "content": f"""
Generate 5 flashcards from this study material.

Return ONLY this format:

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

    cleaned_response = (
        content_response
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        flashcards = json.loads(
            cleaned_response
        )

        return flashcards

    except Exception as e:
        print(e)

        return []


def generate_quiz(
    content: str
):
    truncated_content = content[:1500]

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "Return ONLY valid JSON.\n"
                    "No markdown.\n"
                    "No explanations.\n"
                    "No extra text.\n"
                    "Output must be a JSON array."
                )
            },
            {
                "role": "user",
                "content": f"""
Create 3 quiz questions from this text.

Format:

[
  {{
    "question": "Question here",
    "option_a": "Option A",
    "option_b": "Option B",
    "option_c": "Option C",
    "option_d": "Option D",
    "correct_answer": "A"
  }}
]

Text:
{truncated_content}
"""
            }
        ]
    )

    content_response = (
        response["message"]["content"]
    )

    cleaned_response = (
        content_response
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        quiz = json.loads(
            cleaned_response
        )

        return quiz

    except Exception as e:
        print(e)

        return []


def chat_with_document(
    document_id: int,
    question: str
):
    relevant_chunks = (
        search_similar_chunks(
            query=question,
            document_id=document_id
        )
    )

    context = "\n\n".join(
        relevant_chunks
    )

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI study assistant.\n"
                    "Answer ONLY using the provided context.\n"
                    "Be concise and clear.\n"
                    "Do not repeat information.\n"
                    "Use short paragraphs.\n"
                    "If the answer is not in the context, say you do not know."
                )
            },
            {
                "role": "user",
                "content": f"""
Context:

{context}

Question:
{question}

Answer:
"""
            }
        ]
    )

    return (
        response["message"]["content"]
    )


def stream_chat_with_document(
    document_id: int,
    question: str
):
    relevant_chunks = (
        search_similar_chunks(
            query=question,
            document_id=document_id
        )
    )

    context = "\n\n".join(
        relevant_chunks
    )

    stream = ollama.chat(
        model=MODEL_NAME,
        stream=True,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI study assistant.\n"
                    "Answer ONLY using the provided context.\n"
                    "Be concise and clear.\n"
                    "Do not repeat information.\n"
                    "Use short paragraphs.\n"
                    "Only answer what the user asked.\n"
                    "If the answer is not in the context, say you do not know."
                )
            },
            {
                "role": "user",
                "content": f"""
Context:

{context}

Question:
{question}

Answer:
"""
            }
        ]
    )

    return stream