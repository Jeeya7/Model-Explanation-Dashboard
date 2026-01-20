# decision_tree.py
# -----------------
# Professional Decision Tree implementation for classification tasks.
# Author: Jiya Pradhan
#
# This module defines a custom, interpretable decision tree classifier using entropy-based splitting
# and information gain. It is intended for educational use and portfolio demonstration, providing
# clear structure and extensibility for further research or production adaptation.
from __future__ import annotations
import numpy as np


# Tree growth hyperparameters
MAX_DEPTH = 3  # Maximum allowed depth for the tree
MIN_SAMPLES_PER_LEAF = 2  # Minimum samples required to form a leaf node


class Node:
    """
    Represents a node in the decision tree.
    Internal nodes store splitting criteria; leaf nodes store prediction results.
    """
    def __init__(self, 
                 feature : int | None = None, 
                 threshold: float | None = None, 
                 left : "Node" | None = None, 
                 right: "Node" | None = None, 
                 value : int | None = None, 
                 IG : float | None = None,
                 samples : int | None = None,
                 class_counts : dict[int, int] | None = None,
                 predicted_class: int | None = None 
        ):
        self.feature = feature      # Feature index used for splitting (None for leaf)
        self.threshold = threshold  # Threshold value for split (None for leaf)
        self.left = left            # Left child node (None for leaf)
        self.right = right          # Right child node (None for leaf)
        self.value = value          # Predicted class label (for leaf nodes)
        self.IG = IG                # Information gain for the split
        self.samples = samples      # Number of samples at this node
        self.class_counts = class_counts  # Class distribution at this node
        self.predicted_class = predicted_class  # Predicted class at this node

    def is_leaf(self):
        """
        Returns True if the node is a leaf node (contains a prediction).
        """
        return self.value is not None
    
    

class DecisionTree:
    """
    Decision Tree classifier for supervised classification tasks.
    Utilizes entropy and information gain to determine optimal splits.
    Provides methods for training and prediction.
    """

    def __init__(self, 
                 max_depth: int | None = None,
                 min_samples_per_leaf: int | None = None,
                 root: Node | None = None
                 ):
        """
        Initialize the DecisionTree classifier.
        Args:
            root (Node, optional): Root node of the tree. Defaults to None.
            max_depth (int, optional): Max Depth of the tree. Defaults to MAX_DEPTH.
            min_samples_per_leaf (int, optional): Minimum samples per leaf. Defaults to MIN_SAMPLES_PER_LEAF.
        """
        self.root = root  # Root node of the tree
        self.max_depth = max_depth if max_depth is not None else MAX_DEPTH
        self.min_samples_per_leaf = min_samples_per_leaf if min_samples_per_leaf is not None else MIN_SAMPLES_PER_LEAF

    def calculate_entropy(self, labels : np.ndarray):
        """
        Compute the entropy for a set of class labels.
        Args:
            labels (np.ndarray): Array of class labels.
        Returns:
            float: Entropy value.
        """
        if len(labels) == 0:
            return 0.0
        
        _, counts = np.unique(labels, return_counts=True)
        p = counts / counts.sum()
        return -np.sum(p * np.log2(p))

    def determine_threshold(self, 
                            features : np.ndarray, 
                            labels : np.ndarray):
        """
        Identify the optimal feature and threshold for splitting, maximizing information gain.
        Args:
            features (np.ndarray): Feature matrix.
            labels (np.ndarray): Class labels.
        Returns:
            tuple: (best_threshold, best_feature_index, max_information_gain)
        """
        dataset_entropy = self.calculate_entropy(labels)
        IG = []
        thresholds = []
        features = np.array(features)
        for feature in range(len(features[0])):
            features_sorted = np.sort(features[:, feature])
            features_unique = np.unique(features_sorted)
            feature_thresholds = []
            IG_per_feature = []
            for i in range(len(features_unique) - 1):
                left, right = features_unique[i], features_unique[i + 1]
                feature_threshold = (left + right) / 2
                feature_thresholds.append(feature_threshold)
                labels_left = []
                labels_right = []
                for j in range(len(features)):
                    if features[j][feature] <= feature_threshold:
                        labels_left.append(labels[j])
                    else:
                        labels_right.append(labels[j])
                # Calculate Information Gain
                left_entropy = self.calculate_entropy(labels_left)
                right_entropy = self.calculate_entropy(labels_right)
                len_labels_left = len(labels_left)
                len_labels_right = len(labels_right)
                total_labels = len_labels_left + len_labels_right
                weighted_entropy_left = (len_labels_left / total_labels) * left_entropy
                weighted_entropy_right = (len_labels_right / total_labels) * right_entropy
                weighted_entropy = weighted_entropy_left + weighted_entropy_right
                ig = dataset_entropy - weighted_entropy
                IG_per_feature.append(ig)
            max_info_gain = max(IG_per_feature)
            IG.append(max_info_gain)
            index_of_max_IG = IG_per_feature.index(max_info_gain)
            threshold = feature_thresholds[index_of_max_IG]
            thresholds.append(threshold)
        max_IG = max(IG)
        index_of_max_IG = IG.index(max_IG)
        max_threshold = thresholds[index_of_max_IG]
        feature_to_split = index_of_max_IG
        return max_threshold, feature_to_split, max_IG

    def split(self, 
              features : np.ndarray, 
              feature_to_split_on : int, 
              threshold : float, 
              labels : np.ndarray):
        """
        Partition the dataset into left and right branches using a feature and threshold.
        Args:
            features (np.ndarray): Feature matrix.
            feature_to_split_on (int): Index of the feature to split on.
            threshold (float): Threshold value for the split.
            labels (np.ndarray): Class labels.
        Returns:
            tuple: (left_features, right_features, left_labels, right_labels)
        """
        left_features = []
        right_features = []
        left_labels = []
        right_labels = []
        for i in range(len(features)):
            feature = features[i][feature_to_split_on]
            if feature <= threshold:
                left_features.append(features[i])
                left_labels.append(labels[i])
            else:
                right_features.append(features[i])
                right_labels.append(labels[i])
        return left_features, right_features, left_labels, right_labels

    @staticmethod
    def stopping_criteria(labels: np.ndarray, 
                          depth: int,
                          max_depth: int):
        """
        Evaluate whether the tree should stop splitting further.
        Args:
            labels (np.ndarray): Class labels.
            depth (int): Current depth of the tree.
            max_depth (int): Max depth of the tree.
        Returns:
            bool: True if stopping criteria are met, False otherwise.
        """
        if len(np.unique(labels)) <= 1:
            return True
        if depth >= max_depth:
            return True
        return False

    def fit(self, features : np.ndarray, labels : np.ndarray):
        """
        Train the decision tree using the provided features and labels.
        Args:
            features (np.ndarray): Feature matrix.
            labels (np.ndarray): Class labels.
        """
        root = Node()
        self.root = root
        self.root = self.__build__(self.root, features, labels)
        
    def __class_count__(self, labels: np.ndarray) -> dict[int, int]:
        """
        Count the occurrences of each class label in the dataset.
        Args:
            labels (np.ndarray): Array of class labels.
        Returns:
            dict[int, int]: Mapping from class label to count.
        """
        values, counts = np.unique(labels, return_counts=True)
        return dict(zip(values, counts))


    def __build__(self, 
                  node : Node, 
                  features : np.ndarray, 
                  labels : np.ndarray, 
                  depth : int = 0):
        """
        Recursively construct the decision tree structure.
        Args:
            node (Node): Current node.
            features (np.ndarray): Feature matrix.
            labels (np.ndarray): Class labels.
            depth (int): Current depth in the tree.
        Returns:
            Node: The constructed node (leaf or internal).
        """
        if DecisionTree.stopping_criteria(labels, depth, self.max_depth):
            # Assign the majority class as the value for the leaf node
            node.class_counts = self.__class_count__(labels)
            node.value = max(node.class_counts, key=node.class_counts.get)
            node.samples = len(labels)
            node.predicted_class = max(node.class_counts, key=node.class_counts.get)
            return node

        threshold, feature_to_split_on, IG = self.determine_threshold(features, labels)
        
        if IG <= 0.1:
            # If information gain is too low, make this a leaf node
            node.class_counts = self.__class_count__(labels)
            node.value = max(node.class_counts, key=node.class_counts.get)
            node.samples = len(labels)
            node.predicted_class = max(node.class_counts, key=node.class_counts.get)
            node.IG = IG
            return node
        
        left_feature, right_feature, left_labels, right_labels = self.split(features, feature_to_split_on, threshold, labels)
        
        if len(left_labels) < self.min_samples_per_leaf or len(right_labels) < self.min_samples_per_leaf:
            # If a split would result in a leaf with too few samples, make this a leaf node
            node.class_counts = self.__class_count__(labels)
            node.value = max(node.class_counts, key=node.class_counts.get)
            node.samples = len(labels)
            node.predicted_class = max(node.class_counts, key=node.class_counts.get)
            node.IG = IG
            return node
        
        node.feature = feature_to_split_on
        node.threshold = threshold
        node.IG = IG
        node.samples = len(labels)
        node.class_counts = self.__class_count__(labels)
        node.predicted_class = max(node.class_counts, key=node.class_counts.get)
        
        left_node = Node()
        right_node = Node()
        
        node.left = self.__build__(left_node, left_feature, left_labels, depth + 1)
        node.right = self.__build__(right_node, right_feature, right_labels, depth + 1)
        return node

    def __traverse__(self, node : Node, x : np.ndarray):
        """
        Traverse the tree to predict the class label for a single sample.
        Args:
            node (Node): Current node in the tree.
            x (np.ndarray): Feature vector for a single sample.
        Returns:
            int: Predicted class label.
        """
        if node.is_leaf():
            return node.value
        if x[node.feature] <= node.threshold:
            # Traverse left subtree
            return self.__traverse__(node.left, x)
        else:
            # Traverse right subtree
            return self.__traverse__(node.right, x)

    def predict(self, X : np.ndarray):
        """
        Predict class labels for multiple samples.
        Args:
            X (np.ndarray): Feature matrix.
        Returns:
            list: Predicted class labels for each sample.
        """
        return [self.__traverse__(self.root, X[i]) for i in range(len(X))]

    def predict_one(self, x : np.ndarray):
        """
        Predict the class label for a single sample.
        Args:
            x (np.ndarray): Feature vector for a single sample.
        Returns:
            int: Predicted class label.
        """
        return self.__traverse__(self.root, x)

        
        