from backend.models import decision_tree as tree
from backend.dashboard import dto

def predict(Tree: tree.DecisionTree, x):
    pred, path = Tree.predict_one(x)
    pred_dto = dto.PredictionDTO(pred, path)
    return pred_dto