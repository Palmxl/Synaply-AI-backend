from pydantic import BaseModel

from typing import List


class DashboardAnalytics(
    BaseModel
):
    total_documents: int

    total_flashcards: int

    total_quizzes: int

    total_chat_messages: int

    recent_activity: List[str]