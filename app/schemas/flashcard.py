from pydantic import BaseModel


class FlashcardResponse(BaseModel):
    id: int
    question: str
    answer: str

    class Config:
        from_attributes = True