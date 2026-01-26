from backend.models.decision_tree import DecisionTree as tree
from backend.dashboard import dto
from backend.dashboard.tree_importer import tree_importer
from backend.dashboard.pred_exporter import predict

def prediction_service(Tree : dto.TreeResponseDTO, feature_list : list):
    backend_tree = tree_importer(Tree)
    return predict(backend_tree, feature_list)
    