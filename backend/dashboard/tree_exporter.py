from backend.models import decision_tree as tree
from backend.dashboard import dto
from collections import deque


def export_tree(
    tree: tree.DecisionTree, 
    feature_names: list[str],
    label_names: list[str],
    confusion_matrix,
    confusion_matrix_metadata):
    
    dto_nodes = []
    dto_edges = []
    
    dto_nodes, dto_edges = __walk__(tree.root, dto_nodes, dto_edges)
    dto_response = dto.TreeResponseDTO()
    dto_response.edges = dto_edges
    dto_response.nodes = dto_nodes
    dto_response.feature_names = feature_names
    dto_response.confusion_matrix = confusion_matrix
    dto_response.confusion_matrix_metadata = confusion_matrix_metadata
    
    if tree.root is None:
        dto_response.root_id = None
        dto_response.nodes = []
        dto_response.edges = []
        return dto_response

    else:
        dto_response.root_id = 0
        
    dto_response.label_names = label_names
    
    return dto_response

def __buildnode__(node: tree.Node, 
                  dto_node: dto.TreeNodeDTO, 
                  id: int, 
                  depth: int):
    
    dto_node.id = id
    dto_node.feature = node.feature
    dto_node.threshold = node.threshold
    dto_node.value = node.value
    dto_node.information_gain = node.IG
    dto_node.is_leaf = node.is_leaf()
    dto_node.samples = node.class_counts
    dto_node.depth = depth
    dto_node.predicted_class = node.predicted_class
    
    return dto_node

def __buildedge__(parent_id, child_id, threshold, feature, branch):
    
    new_edge = dto.TreeEdgeDTO()
    new_edge.branch = branch
    new_edge.source = parent_id
    new_edge.target = child_id
    
    if branch == "left":
        operator = "<="
    else:
        operator = ">"
        
    new_edge.operator = operator
    new_edge.feature = feature
    new_edge.threshold = threshold
    
    return new_edge
    
    
    
def __walk__(root_node: tree.Node, dto_nodes, dto_edges):

    queue = deque([(root_node, 0)])
    node_to_id = {}
    node_to_id[root_node] = 0
    next_id = 1
    
    while (queue):
        
        curr_node, depth = queue.popleft()
        new_dto_node = dto.TreeNodeDTO()
        new_dto_node = __buildnode__(curr_node, 
                                     new_dto_node, 
                                     node_to_id[curr_node], 
                                     depth)
        
        if curr_node.left is not None:
            if curr_node.left not in node_to_id:
                node_to_id[curr_node.left] = next_id
                next_id += 1
                queue.append((curr_node.left, depth+1))

            dto_edges.append(__buildedge__(node_to_id[curr_node],
                                        node_to_id[curr_node.left],
                                        curr_node.threshold,
                                        curr_node.feature,
                                        "left"))
            new_dto_node.left_id = node_to_id[curr_node.left]
        else:
            new_dto_node.left_id = None

            
        if curr_node.right is not None:
            if curr_node.right not in node_to_id:
                node_to_id[curr_node.right] = next_id
                next_id += 1
                queue.append((curr_node.right, depth+1))

            dto_edges.append(__buildedge__(node_to_id[curr_node],
                                        node_to_id[curr_node.right],
                                        curr_node.threshold,
                                        curr_node.feature,
                                        "right"))
            new_dto_node.right_id = node_to_id[curr_node.right]
        else:
            new_dto_node.right_id = None

        dto_nodes.append(new_dto_node)
    
    
    return dto_nodes, dto_edges
        
        