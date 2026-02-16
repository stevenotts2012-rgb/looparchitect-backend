from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI()

# Allow Railway healthcheck host
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

