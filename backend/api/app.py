from fastapi import FastAPI
from backend.api.routers import router 

app = FastAPI()
app.include_router(router)