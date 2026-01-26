from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.tree_service import tree_service
from backend.services.prediction_service import prediction_service
from typing import Any

router = APIRouter()


@router.get("/", status_code=200)
def health_check():
    return {"status": "ok"}

@router.post("/api/train")
def train():
    return tree_service()

class PredictRequest(BaseModel):
    tree: dict[str, Any]
    x: list[float]

@router.post("/api/predict")
def predict(req: PredictRequest):
    x = req.x
    tree = req.tree
    return prediction_service(tree, x)