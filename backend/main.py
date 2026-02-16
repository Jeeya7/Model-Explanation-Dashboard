from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routers import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://jeeya7.github.io/Model-Explanation-Dashboard/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
