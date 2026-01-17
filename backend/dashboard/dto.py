class TreeNodeDTO:
    def __init__(
        self,
        id: int,
        feature: str | None,
        threshold: float | None,
        value: str | None,
        information_gain: float | None,
        is_leaf: bool
    ):
        self.id = id
        self.feature = feature
        self.threshold = threshold
        self.value = value
        self.information_gain = information_gain
        self.is_leaf = is_leaf

        
class TreeEdgeDTO:
    def __init__(self, source: int, target: int, condition: str):
        self.source = source
        self.target = target
        self.condition = condition  # "≤ threshold" or "> threshold"
        
class MetricsDTO:
    def __init__(
        self,
        accuracy: float,
        precision: float | None = None,
        recall: float | None = None,
        f1: float | None = None
    ):
        self.accuracy = accuracy
        self.precision = precision
        self.recall = recall
        self.f1 = f1

class TreeResponseDTO:
    def __init__(
        self,
        nodes: list[TreeNodeDTO],
        edges: list[TreeEdgeDTO],
        metrics: MetricsDTO
    ):
        self.nodes = nodes
        self.edges = edges
        self.metrics = metrics




