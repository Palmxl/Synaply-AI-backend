from fastapi import FastAPI

app = FastAPI(
    title="Synaply AI",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Synaply AI Backend Running"}