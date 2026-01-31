from __future__ import annotations
from typing import Any
import math

def _json_safe(x: Any) -> Any:
    """
    Recursively convert an object to a JSON-safe representation.
    Handles NumPy types, Python built-ins, and nested structures.
    Args:
        x (Any): The object to convert.
    Returns:
        Any: JSON-safe version of the input.
    """
    if x is None:
        return None

    # Handle NumPy scalars/arrays (works even if numpy isn't imported)
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

    # Handle standard Python types
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

    # Fallback: convert to string
    return str(x)

class TreeNodeDTO:
    """
    Data Transfer Object representing a node in a decision tree.

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
        self.feature = feature  # Index of splitting feature (None for leaves)
        self.threshold = threshold  # Threshold value for split (None for leaves)
        self.value = value  # Class label or value (for leaves)
        self.information_gain = information_gain  # Information gain from split (None for leaves)
        self.is_leaf = is_leaf  # Indicates if node is a leaf
        self.samples = samples  # Number of samples at node
        self.class_counts = class_counts  # Class distribution at node
        self.depth = depth  # Depth of node in tree
        self.predicted_class = predicted_class  # Predicted class at node
        self.left_id = left_id  # Id of the left child
        self.right_id = right_id  # Id of the right child
        
    def to_dict(self) -> dict[str, Any]:
        """
        Convert the TreeNodeDTO to a JSON-serializable dictionary.
        Returns:
            dict[str, Any]: Dictionary representation of the node.
        """
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
            "right_id": str(self.right_id) if self.right_id is not None else None
            
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
    Data Transfer Object representing an edge between decision tree nodes.

    Attributes:
        source (int): Source node identifier.
        target (int): Target node identifier.
        branch (str): Indicates which branch this edge represents ("left" or "right").
        operator (str): The comparison operator used for the split ("<=" for left, ">" for right).
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
        self.branch = branch  # Branch identifier ("left" or "right")
        self.operator = operator  # Comparison operator ("<=", ">")
        self.feature = feature  # Index of feature used for split
        self.threshold = threshold  # Threshold value for split
    
    def to_dict(self) -> dict[str, Any]:
        """
        Convert the TreeEdgeDTO to a JSON-serializable dictionary.
        Returns:
            dict[str, Any]: Dictionary representation of the edge.
        """
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


class TreeResponseDTO:
    """
    Data Transfer Object for decision tree response, including structure and metrics.

    Attributes:
        root_id (int): Root node identifier.
        nodes (list[TreeNodeDTO]): List of tree nodes.
        edges (list[TreeEdgeDTO]): List of tree edges.
        feature_names (list[str]): List of feature names in dataset.
        label_names (list[str]): List of label/class names in dataset.
    """
    def __init__(
        self,
        confusion_matrix = None,
        confusion_matrix_metadata = None,
        root_id: int = None,
        nodes: list[TreeNodeDTO] = None,
        edges: list[TreeEdgeDTO] = None,
        feature_names: list[str] = None,
        label_names: list[str] = None,
    ):
        self.nodes = nodes  # List of tree nodes
        self.edges = edges  # List of tree edges
        self.root_id = root_id  # Root node identifier
        self.feature_names = feature_names  # List of feature names
        self.label_names = label_names  # List of label/class names
        self.confusion_matrix = confusion_matrix # List of values for confusion matrix
        self.confusion_matrix_metadata = confusion_matrix_metadata # Dict of metadata for conf_matrix
        
    def to_dict(self) -> dict[str, Any]:
        """
        Convert the TreeResponseDTO to a JSON-serializable dictionary.
        Returns:
            dict[str, Any]: Dictionary representation of the tree response.
        """
        return {
            "root_id": str(self.root_id) if self.root_id is not None else None,
            "nodes": [] if not self.nodes else [n.to_dict() for n in self.nodes],
            "edges": [] if not self.edges else [e.to_dict() for e in self.edges],
            "feature_names": [] if self.feature_names is None else list(self.feature_names),
            "label_names": [] if self.label_names is None else list(self.label_names),
            "confusion_matrix": _json_safe(self.confusion_matrix),
            "confusion_matrix_metadata": _json_safe(self.confusion_matrix_metadata),
        }

    def __repr__(self) -> str:
        n = 0 if not self.nodes else len(self.nodes)
        e = 0 if not self.edges else len(self.edges)
        return f"TreeResponseDTO(root_id={self.root_id}, nodes={n}, edges={e})"


class PredictionDTO:
    """
    Data Transfer Object for a single prediction result.

    Attributes:
        predicted_class (int | None): Predicted class label.
        path (list[int] | None): List of node IDs representing the path taken in the tree.
    """
    def __init__(self,
                 predicted_class: int | None = None,
                 path: list[int] | None = None):
        self.predicted_class = predicted_class  # Predicted class label
        self.path = path  # Path of node IDs traversed for this prediction

