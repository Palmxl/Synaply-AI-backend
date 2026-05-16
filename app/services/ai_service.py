import ollama

import json

from app.services.vector_service import (
    search_similar_chunks
)

def generate_summary(
    content: str
):
    truncated_content = content[:2500]

    response = ollama.chat(
        model="phi3",
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
        model="phi3",
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
    
def generate_quiz(
    content: str
):
    truncated_content = content[:2500]

    response = ollama.chat(
        model="phi3",
        messages=[
            {
                "role": "system",
                "content": (
                    "Generate 5 multiple choice questions "
                    "in valid JSON format only."
                )
            },
            {
                "role": "user",
                "content": f"""
Generate a quiz from this study material.

Return ONLY this format:

[
  {{
    "question": "...",
    "option_a": "...",
    "option_b": "...",
    "option_c": "...",
    "option_d": "...",
    The correct_answer MUST ONLY be:
    "A", "B", "C", or "D"
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
        quiz = json.loads(
            content_response
        )

        return quiz

    except:
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
        model="phi3",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI study assistant. "
                    "Answer questions ONLY using the retrieved context."
                )
            },
            {
                "role": "user",
                "content": f"""
Context:

{context}

Question:
{question}
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
        model="phi3",
        stream=True,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI study assistant. "
                    "Answer ONLY using the provided context."
                )
            },
            {
                "role": "user",
                "content": f"""
Context:

{context}

Question:
{question}
"""
            }
        ]
    )

    return stream