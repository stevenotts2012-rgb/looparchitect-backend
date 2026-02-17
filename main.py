import os
from typing import Optional
import json
from openai import OpenAI

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
client = OpenAI()


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
    # 1) Defaults (fallbacks)
    defaults = {
        "bpm": 140,
        "key": "F minor",
        "scale": "Natural Minor",
        "mood": "Dark",
        "energy": "High",
        "genre": "Trap",
        "loop_length_bars": 8,
    }

    # 2) User overrides (anything user sends wins)
    user_data = data.model_dump(exclude_unset=True)

    # 3) Ask OpenAI ONLY for the missing fields
    missing_fields = [k for k in defaults.keys() if k not in user_data]

    # If user provided everything, just return it merged with defaults (user wins)
    if not missing_fields:
        return {**defaults, **user_data}

    schema = {
        "type": "object",
        "properties": {
            "bpm": {"type": "integer", "minimum": 60, "maximum": 200},
            "key": {"type": "string"},
            "scale": {"type": "string"},
            "mood": {"type": "string"},
            "energy": {"type": "string"},
            "genre": {"type": "string"},
            "loop_length_bars": {"type": "integer", "minimum": 2, "maximum": 64},
        },
        "required": missing_fields,
        "additionalProperties": False,
    }

    prompt = f"""
You are generating structured music parameters for a beat generator app.

Return ONLY valid JSON matching the schema.
Fill ONLY these missing fields: {missing_fields}

Context:
- If genre is missing, infer a mainstream-friendly genre that fits the user's provided fields.
- Keep results practical for producers.

User provided:
{json.dumps(user_data, indent=2)}
""".strip()

    # 4) Call OpenAI Responses API with strict JSON schema output
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    resp = client.responses.create(
        model=model,
        input=prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "looparchitect_generate",
                "description": "Generate missing beat parameters.",
                "schema": schema,
                "strict": True,
            }
        },
        temperature=0.4,
    )

    ai_json = json.loads(resp.output_text)

    # 5) Merge: defaults -> AI fills -> user overrides last (user always wins)
    final_output = {**defaults, **ai_json, **user_data}
    return final_output

    user_data = data.model_dump(exclude_unset=True)
    final_output = {**defaults, **user_data}
    return final_output


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
