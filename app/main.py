from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from app.db.database import (
    Base,
    engine
)

from app.api.routes import auth
from app.api.routes import documents
from app.api.routes import ai
from app.api.routes import flashcards
from app.api.routes import quizzes
from app.api.routes import chat
from app.api.routes import websocket
from app.api.routes import dashboard


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Synaply AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://synaply-ai-frontend.vercel.app",
        "https://palmxl.github.io",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)

app.include_router(
    documents.router,
    prefix="/api/v1/documents",
    tags=["Documents"]
)

app.include_router(
    ai.router,
    prefix="/api/v1/ai",
    tags=["AI"]
)

app.include_router(
    flashcards.router,
    prefix="/api/v1/flashcards",
    tags=["Flashcards"]
)

app.include_router(
    quizzes.router,
    prefix="/api/v1/quizzes",
    tags=["Quizzes"]
)

app.include_router(
    chat.router,
    prefix="/api/v1/chat",
    tags=["AI Chat"]
)

app.include_router(
    websocket.router
)

app.include_router(
    dashboard.router,
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)


@app.get("/")
def root():
    return {
        "message": "Synaply AI Backend Running"
    }