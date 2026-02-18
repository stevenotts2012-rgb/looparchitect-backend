11  import os
2  import json
3  from typing import Optional
4
5  from fastapi import FastAPI
6  from pydantic import BaseModel
7  import uvicorn
8
9  app = FastAPI()
10
11
12 class GenerateRequest(BaseModel):
13     bpm: Optional[int] = None
14     key: Optional[str] = None
15     scale: Optional[str] = None
16     mood: Optional[str] = None
17     energy: Optional[str] = None
18     genre: Optional[str] = None
19     loop_length_bars: Optional[int] = None
20
21
22 @app.get("/")
23 def root():
24     return {"status": "ok"}
25
26
27 @app.get("/health")
28 def health():
29     return {"ok": True}
30
31
32 def _defaults():
33     return {
34         "bpm": 140,
35         "key": "F minor",
36         "scale": "Natural Minor",
37         "mood": "Dark",
38         "energy": "High",
39         "genre": "Trap",
40         "loop_length_bars": 8,
41     }
42
43
44 @app.post("/generate")
45 async def generate(data: GenerateRequest):
46     defaults = _defaults()
47     user_data = data.model_dump(exclude_unset=True)
48
49     # If user provided everything, just return merged output
50     missing_fields = [k for k in defaults.keys() if k not in user_data]
51     if not missing_fields:
52         return {**defaults, **user_data}
53
54     # If there is no OpenAI key set, do NOT crash — return defaults + user overrides
55     api_key = os.environ.get("OPENAI_API_KEY", "").strip()
56     if not api_key:
57         return {**defaults, **user_data}
58
59     # Try OpenAI (safe fallback if anything goes wrong)
60     try:
61         from openai import OpenAI  # imported here so deploy won't fail if package missing
62         client = OpenAI(api_key=api_key)
63
64         schema = {
65             "type": "object",
66             "properties": {
67                 "bpm": {"type": "integer", "minimum": 60, "maximum": 200},
68                 "key": {"type": "string"},
69                 "scale": {"type": "string"},
70                 "mood": {"type": "string"},
71                 "energy": {"type": "string"},
72                 "genre": {"type": "string"},
73                 "loop_length_bars": {"type": "integer", "minimum": 2, "maximum": 64},
74             },
75             "required": missing_fields,
76             "additionalProperties": False,
77         }
78
79         prompt = f"""
80 You generate structured music parameters for a beat generator app.
81 Return ONLY valid JSON matching the schema, filling ONLY these missing fields: {missing_fields}
82
83 User provided:
84 {json.dumps(user_data, indent=2)}
85 """.strip()
86
87         model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
88         resp = client.responses.create(
89             model=model,
90             input=prompt,
91             text={
92                 "format": {
93                     "type": "json_schema",
94                     "name": "looparchitect_generate",
95                     "schema": schema,
96                     "strict": True,
97                 }
98             },
99             temperature=0.4,
100        )
101
102        ai_json = json.loads(resp.output_text)
103        return {**defaults, **ai_json, **user_data}  # user always wins
104
105    except Exception:
106        # Never crash the service if AI call fails
107        return {**defaults, **user_data}
108
109
110 if __name__ == "__main__":
111     port = int(os.environ.get("PORT", "8000"))
112     uvicorn.run(app, host="0.0.0.0", port=port)
