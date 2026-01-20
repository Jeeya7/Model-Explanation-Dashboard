from __future__ import annotations
from typing import Any
import math

def _json_safe(x: Any) -> Any:
    if x is None:
        return None

    # ---- NumPy scalars / arrays (works even if numpy isn't imported)
    tname = type(x).__name__
    if hasattr(x, "item") and tname.startswith(("int", "float", "bool", "str")):
        try:
            return _json_safe(x.item())
        except Exception:
            pass
    if hasattr(x, "tolist"):
        try:
            return _json_safe(x.tolist())
        except Exception:
            pass

    # ---- normal python
    if isinstance(x, (str, int, bool)):
        return x
    if isinstance(x, float):
        if math.isnan(x) or math.isinf(x):
            return None
        return x
    if isinstance(x, dict):
        return {str(_json_safe(k)): _json_safe(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json_safe(v) for v in x]

    return str(x)

class TreeNodeDTO:
    """
    Professional DTO representing a node in a decision tree.
    
    Attributes:
        id (int): Unique node identifier.
        feature (int | None): Index of the splitting feature (None for leaves).
        threshold (float | None): Threshold value for split (None for leaves).
        value (int | None): Class label or value (for leaves).
        information_gain (float | None): Information gain from split (None for leaves).
        is_leaf (bool): Indicates if node is a leaf.
        samples (int | None): Number of samples at node.
        class_counts (dict[int, int] | None): Class distribution at node.
        depth (int | None): Depth of node in tree.
        predicted_class (int | None): Predicted class at node.
        left_id (int | None): Id of the left child.
        right_id (int | None): Id of the right child.
    """
    def __init__(
        self,
        id: int = None,
        feature: int | None = None,
        threshold: float | None = None,
        value: int | None = None,
        information_gain: float | None = None,
        is_leaf: bool = None,
        samples: int | None = None,
        class_counts: dict[int, int] | None = None,
        depth: int | None = None,
        predicted_class: int | None = None,
        left_id: int | None = None,
        right_id: int | None = None
        
    ):
        self.id = id  # Unique node identifier
        self.feature = feature  # Index of splitting feature
        self.threshold = threshold  # Threshold value for split
        self.value = value  # Class label or value (for leaves)
        self.information_gain = information_gain  # Information gain from split
        self.is_leaf = is_leaf  # Indicates if node is a leaf
        self.samples = samples  # Number of samples at node
        self.class_counts = class_counts  # Class distribution at node
        self.depth = depth  # Depth of node in tree
        self.predicted_class = predicted_class  # Predicted class at node
        self.left_id = left_id # Id of the left child
        self.right_id = right_id # Id of the right child
        
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": str(self.id) if self.id is not None else None,
            "feature": self.feature,
            "threshold": _json_safe(self.threshold),
            "value": None if self.value is None else int(self.value),
            "information_gain": _json_safe(self.information_gain),
            "is_leaf": self.is_leaf,
            "samples": None if self.samples is None else {int(k): int(v) for k, v in self.samples.items()},
            "class_counts": None if self.class_counts is None else {int(k): int(v) for k, v in self.class_counts.items()},
            "depth": None if self.depth is None else int(self.depth),
            "predicted_class": None if self.predicted_class is None else int(self.predicted_class),
            "left_id": str(self.left_id) if self.left_id is not None else None,
            "right_id": str(self.right_id) if self.right_id is not None else None,
        }

    def __repr__(self) -> str:
        # optional: makes debugging prints readable
        return (
            f"TreeNodeDTO(id={self.id}, depth={self.depth}, "
            f"is_leaf={self.is_leaf}, feature={self.feature}, "
            f"threshold={self.threshold}, predicted_class={self.predicted_class})"
        )
        
class TreeEdgeDTO:
    """
    Professional DTO representing an edge between decision tree nodes.
    
    Attributes:
        source (int): Source node identifier.
        target (int): Target node identifier.
        branch (str): Indicates which branch this edge represents ("left" or "right").
        operator (str): The comparison operator used for the split ("<=" for left, ">" for right)..
        feature (int): Index of the feature used for the split at this edge.
        threshold (float): Threshold value for the split at this edge.
    """
    def __init__(self, 
                 source: int = None, 
                 target: int = None, 
                 branch: str = None,
                 operator: str = None,
                 feature: int = None,
                 threshold: float = None):
        self.source = source  # Source node identifier
        self.target = target  # Target node identifier
        self.branch = branch  # Branch identifier
        self.operator = operator # Comparison Operator
        self.feature = feature # Index of feature used for split
        self.threshold = threshold # Threshold value for split
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "source": str(self.source) if self.source is not None else None,
            "target": str(self.target) if self.target is not None else None,
            "branch": self.branch,
            "operator": self.operator,
            "feature": self.feature,
            "threshold": _json_safe(self.threshold),
        }

    def __repr__(self) -> str:
        return (
            f"TreeEdgeDTO(source={self.source}, target={self.target}, "
            f"branch={self.branch}, op={self.operator}, "
            f"feature={self.feature}, threshold={self.threshold})"
        )
        
class MetricsDTO:
    """
    Professional DTO for model evaluation metrics.
    
    Attributes:
        accuracy (float): Model accuracy.
        precision (float | None): Precision (optional).
        recall (float | None): Recall (optional).
        f1 (float | None): F1 score (optional).
    """
    def __init__(
        self,
        accuracy: float = None,
        precision: float | None = None,
        recall: float | None = None,
        f1: float | None = None
    ):
        self.accuracy = accuracy  # Model accuracy
        self.precision = precision  # Precision metric
        self.recall = recall  # Recall metric
        self.f1 = f1  # F1 score
        
    def to_dict(self) -> dict[str, Any]:
        return {
            "accuracy": _json_safe(self.accuracy),
            "precision": _json_safe(self.precision),
            "recall": _json_safe(self.recall),
            "f1": _json_safe(self.f1),
        }

    def __repr__(self) -> str:
        return (
            f"MetricsDTO(acc={self.accuracy}, prec={self.precision}, "
            f"rec={self.recall}, f1={self.f1})"
        )

class TreeResponseDTO:
    """
    Professional DTO for decision tree response, including structure and metrics.
    
    Attributes:
        root_id (int): Root node identifier.
        nodes (list[TreeNodeDTO]): List of tree nodes.
        edges (list[TreeEdgeDTO]): List of tree edges.
        metrics (MetricsDTO | None): Model evaluation metrics.
        feature_names (list[str]): List of feature names in dataset.
        label_names (list[str]): List of label/class names in dataset.
    """
    def __init__(
        self,
        root_id: int = None,
        nodes: list[TreeNodeDTO] = None,
        edges: list[TreeEdgeDTO] = None,
        metrics: MetricsDTO | None = None,
        feature_names: list[str] = None,
        label_names: list[str] = None
    ):
        self.nodes = nodes  # List of tree nodes
        self.edges = edges  # List of tree edges
        self.metrics = metrics  # Model evaluation metrics
        self.root_id = root_id  # Root node identifier
        self.feature_names = feature_names  # List of feature names
        self.label_names = label_names # List of label/class names
        
    def to_dict(self) -> dict[str, Any]:
        return {
            "root_id": str(self.root_id) if self.root_id is not None else None,
            "nodes": [] if not self.nodes else [n.to_dict() for n in self.nodes],
            "edges": [] if not self.edges else [e.to_dict() for e in self.edges],
            "metrics": None if self.metrics is None else self.metrics.to_dict(),
            "feature_names": [] if self.feature_names is None else list(self.feature_names),
            "label_names": [] if self.label_names is None else list(self.label_names),
        }

    def __repr__(self) -> str:
        n = 0 if not self.nodes else len(self.nodes)
        e = 0 if not self.edges else len(self.edges)
        return f"TreeResponseDTO(root_id={self.root_id}, nodes={n}, edges={e})"




