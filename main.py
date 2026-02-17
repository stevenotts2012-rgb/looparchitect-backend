import os
from typing import Optional

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


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
    defaults = {
        "bpm": 140,
        "key": "F minor",
        "scale": "Natural Minor",
        "mood": "Dark",
        "energy": "High",
        "genre": "Trap",
        "loop_length_bars": 8,
    }

    user_data = data.model_dump(exclude_unset=True)
    final_output = {**defaults, **user_data}
    return final_output


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
