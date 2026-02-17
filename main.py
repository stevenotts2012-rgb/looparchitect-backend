import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


class GenerateRequest(BaseModel):
    test: str


@app.get("/")
def root():
    return {"status": "ok"}


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/generate")
async def generate(data: GenerateRequest):
    return {
        "message": "Generate endpoint working",
        "you_sent": data
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
