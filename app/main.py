from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base
from app.db.database import engine

from app.api.routes import auth
from app.api.routes import documents

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Synaply AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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


@app.get("/")
def root():
    return {
        "message": "Synaply AI Backend Running"
    }