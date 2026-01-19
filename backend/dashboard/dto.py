class TreeNodeDTO:
    """
    DTO for a decision tree node.
    
    Fields:
        id (int): Node ID.
        feature (int | None): Splitting feature index (None for leaves).
        threshold (float | None): Split threshold (None for leaves).
        value (int | None): Class label or value (for leaves).
        information_gain (float | None): Info gain from split (None for leaves).
        is_leaf (bool): True if leaf node.
        samples (int | None): Number of samples at node.
        class_counts (list[int] | None): Class counts at node.
        depth (int | None): Node depth in tree.
        predicted_class (int | None): Predicted class at node.
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
        class_counts: list[int] | None,
        depth: int | None,
        predicted_class: int | None
        
    ):
        self.id = id  # Node ID
        self.feature = feature  # Splitting feature index
        self.threshold = threshold  # Split threshold
        self.value = value  # Class label or value (for leaves)
        self.information_gain = information_gain  # Information gain from split
        self.is_leaf = is_leaf  # True if leaf node
        self.samples = samples  # Number of samples at node
        self.class_counts = class_counts  # Class counts at node
        self.depth = depth  # Node depth
        self.predicted_class = predicted_class  # Predicted class at node
        
class TreeEdgeDTO:
    """
    DTO for an edge between decision tree nodes.
    
    Fields:
        source (int): Source node ID.
        target (int): Target node ID.
        condition (str): Edge condition (e.g., "≤ threshold", "> threshold").
    """
    def __init__(self, source: int, target: int, condition: str):
        self.source = source  # Source node ID
        self.target = target  # Target node ID
        self.condition = condition  # Edge condition
        
class MetricsDTO:
    """
    DTO for model evaluation metrics.
    
    Fields:
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
        self.accuracy = accuracy  # Accuracy
        self.precision = precision  # Precision
        self.recall = recall  # Recall
        self.f1 = f1  # F1 score

class TreeResponseDTO:
    """
    DTO for decision tree response, including structure and metrics.
    
    Fields:
        root_id (int): Root node ID.
        nodes (list[TreeNodeDTO]): Tree nodes.
        edges (list[TreeEdgeDTO]): Tree edges.
        metrics (MetricsDTO): Model metrics.
        feature_names (list[str]): Feature Names
    """
    def __init__(
        self,
        root_id: int,
        nodes: list[TreeNodeDTO],
        edges: list[TreeEdgeDTO],
        metrics: MetricsDTO,
        feature_names: list[str]
    ):
        self.nodes = nodes  # Tree nodes
        self.edges = edges  # Tree edges
        self.metrics = metrics  # Model metrics
        self.root_id = root_id  # Root node ID
        self.feature_names = feature_names # Feature Names of Dataset




