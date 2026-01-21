from fastapi import APIRouter
from backend.services.tree_service import tree_service

router = APIRouter()
    

@router.get("/", status_code=200)
def health_check():
    return {"status": "ok"}

@router.post("/api/train")
def train():
    return tree_service()