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
        id: int,
        feature: int | None,
        threshold: float | None,
        value: int | None,
        information_gain: float | None,
        is_leaf: bool,
        samples: int | None,
        class_counts: dict[int, int] | None,
        depth: int | None,
        predicted_class: int | None,
        left_id: int | None,
        right_id: int | None
        
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
        
class TreeEdgeDTO:
    """
    Professional DTO representing an edge between decision tree nodes.
    
    Attributes:
        source (int): Source node identifier.
        target (int): Target node identifier.
        condition (str): Edge condition (e.g., "≤ threshold", "> threshold").
    """
    def __init__(self, source: int, target: int, condition: str):
        self.source = source  # Source node identifier
        self.target = target  # Target node identifier
        self.condition = condition  # Edge condition
        
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
        accuracy: float,
        precision: float | None = None,
        recall: float | None = None,
        f1: float | None = None
    ):
        self.accuracy = accuracy  # Model accuracy
        self.precision = precision  # Precision metric
        self.recall = recall  # Recall metric
        self.f1 = f1  # F1 score

class TreeResponseDTO:
    """
    Professional DTO for decision tree response, including structure and metrics.
    
    Attributes:
        root_id (int): Root node identifier.
        nodes (list[TreeNodeDTO]): List of tree nodes.
        edges (list[TreeEdgeDTO]): List of tree edges.
        metrics (MetricsDTO | None): Model evaluation metrics.
        feature_names (list[str]): List of feature names in dataset.
    """
    def __init__(
        self,
        root_id: int,
        nodes: list[TreeNodeDTO],
        edges: list[TreeEdgeDTO],
        metrics: MetricsDTO | None,
        feature_names: list[str]
    ):
        self.nodes = nodes  # List of tree nodes
        self.edges = edges  # List of tree edges
        self.metrics = metrics  # Model evaluation metrics
        self.root_id = root_id  # Root node identifier
        self.feature_names = feature_names  # List of feature names




