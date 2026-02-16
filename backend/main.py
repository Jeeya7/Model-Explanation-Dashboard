from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routers import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://jeeya7.github.io",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {"status": "ok", "message": "Backend is running", "docs": "/docs"}

@app.get("/health")
def health():
    return {"ok": True}
