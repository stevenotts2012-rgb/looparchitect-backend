import os
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


from typing import Optional

class GenerateRequest(BaseModel):
    bpm: Optional[int] = None
    key: Optional[str] = None
    scale: Optional[str] = None
    mood: Optional[str] = None
    energy: Optional[str] = None
    genre: Optional[str] = None
    loop_length_bars: Optional[int] = None

    


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
