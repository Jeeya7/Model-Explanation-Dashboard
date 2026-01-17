class TreeNodeDTO:
    """
    Data Transfer Object representing a node in a decision tree.
    
    Attributes:
        id (int): Unique identifier for the node.
        feature (str | None): Feature used for splitting at this node (None for leaves).
        threshold (float | None): Threshold value for the split (None for leaves).
        value (str | None): Value or class label at the node (for leaves).
        information_gain (float | None): Information gain from the split (None for leaves).
        is_leaf (bool): Whether this node is a leaf node.
    """
    def __init__(
        self,
        id: int,
        feature: str | None,
        threshold: float | None,
        value: str | None,
        information_gain: float | None,
        is_leaf: bool
    ):
        self.id = id  # Node identifier
        self.feature = feature  # Splitting feature
        self.threshold = threshold  # Split threshold
        self.value = value  # Class label or value (for leaves)
        self.information_gain = information_gain  # Info gain from split
        self.is_leaf = is_leaf  # True if node is a leaf

        
class TreeEdgeDTO:
    """
    Data Transfer Object representing an edge between two nodes in a decision tree.
    
    Attributes:
        source (int): Source node id.
        target (int): Target node id.
        condition (str): Condition for the edge (e.g., "≤ threshold" or "> threshold").
    """
    def __init__(self, source: int, target: int, condition: str):
        self.source = source  # Source node id
        self.target = target  # Target node id
        self.condition = condition  # Edge condition (split direction)
        
class MetricsDTO:
    """
    Data Transfer Object for model evaluation metrics.
    
    Attributes:
        accuracy (float): Model accuracy.
        precision (float | None): Model precision (optional).
        recall (float | None): Model recall (optional).
        f1 (float | None): F1 score (optional).
    """
    def __init__(
        self,
        accuracy: float,
        precision: float | None = None,
        recall: float | None = None,
        f1: float | None = None
    ):
        self.accuracy = accuracy  # Accuracy metric
        self.precision = precision  # Precision metric
        self.recall = recall  # Recall metric
        self.f1 = f1  # F1 score

class TreeResponseDTO:
    """
    Data Transfer Object for the response containing a decision tree structure and its metrics.
    
    Attributes:
        nodes (list[TreeNodeDTO]): List of tree nodes.
        edges (list[TreeEdgeDTO]): List of edges between nodes.
        metrics (MetricsDTO): Evaluation metrics for the tree/model.
    """
    def __init__(
        self,
        nodes: list[TreeNodeDTO],
        edges: list[TreeEdgeDTO],
        metrics: MetricsDTO
    ):
        self.nodes = nodes  # List of tree nodes
        self.edges = edges  # List of tree edges
        self.metrics = metrics  # Model metrics




