from backend.models.decision_tree import DecisionTree
from backend.models.decision_tree import Node
from typing import Any

def tree_importer(tree: dict[str, Any]) -> DecisionTree:
    """
    tree: the JSON decoded dict (TreeResponseDTO.to_dict() output)
    Returns: DecisionTree with internal Node links wired.
    """

    root_id_raw = tree.get("root_id")
    if root_id_raw is None:
        return DecisionTree(root=None)

    root_id = int(root_id_raw)

    dto_nodes = tree.get("nodes", [])

    # 1) Create all Node objects
    nodes_by_id: dict[int, Node] = {}
    for n in dto_nodes:
        nid = int(n["id"])  # string -> int
        nodes_by_id[nid] = Node(
            id=nid,
            feature=n.get("feature"),
            threshold=n.get("threshold"),
            value=n.get("value"),
            IG=n.get("information_gain"),
            samples=None,  
            class_counts=n.get("class_counts"),
            predicted_class=n.get("predicted_class"),
        )

    # 2) Wire children pointers
    for n in dto_nodes:
        nid = int(n["id"])
        node = nodes_by_id[nid]

        left_id = n.get("left_id")
        right_id = n.get("right_id")

        node.left = nodes_by_id[int(left_id)] if left_id is not None else None
        node.right = nodes_by_id[int(right_id)] if right_id is not None else None

    # 3) Create DecisionTree
    return DecisionTree(root=nodes_by_id[root_id])

