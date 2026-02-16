import os
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*", "healthcheck.railway.app"]
)

@app.get("/")
async def root():
    return {"status": "LoopArchitect backend is live"}

@app.get("/health")
async def health():
    return {"ok": True}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


