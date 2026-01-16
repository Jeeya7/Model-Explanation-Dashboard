
# decision_tree.py
# -----------------
# Custom Decision Tree implementation for classification tasks.
# Author: Jiya Praedhan
# Description: This module provides an interpretable decision tree classifier
#              with entropy-based splitting and information gain. Designed for educational
#              and portfolio demonstration purposes.

import numpy as np
import pandas as pd

# Hyperparameters for tree growth
MAX_DEPTH = 3  # Maximum depth of the tree
MIN_SAMPLES_PER_LEAF = 2  # Minimum samples required to form a leaf node


class Node:
    """
    Represents a single node in the decision tree.
    Internal nodes contain a feature and threshold for splitting.
    Leaf nodes contain a predicted value.
    """
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None, IG=None):
        self.feature = feature      # Index of the feature to split on
        self.threshold = threshold  # Threshold value for the split
        self.left = left            # Left child node
        self.right = right          # Right child node
        self.value = value          # Predicted class (for leaf nodes)
        self.IG = IG                # Information Gain for the split

    def is_leaf(self):
        """Check if the node is a leaf node."""
        return self.value is not None
    
    

class DecisionTree:
    """
    Decision Tree classifier using entropy and information gain for splitting.
    Supports fitting to data and making predictions for classification tasks.
    """

    def __init__(self, root=None):
        """
        Initialize the DecisionTree.
        Args:
            root (Node, optional): Root node of the tree. Defaults to None.
        """
        self.root = root  # The starting point of the tree

    def calculate_entropy(self, features):
        """
        Calculate the entropy of a list of labels.
        Args:
            features (list or array): List of class labels.
        Returns:
            float: Entropy value.
        """
        if len(features) == 0:
            return 0
        y_series = pd.Series(features)
        value_counts = y_series.value_counts()
        prob = value_counts / len(features)
        log_p = [np.log(p) for p in prob]
        prob = np.array(prob)
        log_p = np.array(log_p)
        prod = prob * log_p * -1
        entropy = prod.sum()
        return entropy

    def determine_threshold(self, features, labels):
        """
        Find the best feature and threshold to split on, maximizing information gain.
        Args:
            features (array-like): Feature matrix.
            labels (array-like): Corresponding class labels.
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

    def split(self, features, feature_to_split_on, threshold, labels):
        """
        Split the dataset into left and right branches based on a feature and threshold.
        Args:
            features (array-like): Feature matrix.
            feature_to_split_on (int): Index of the feature to split on.
            threshold (float): Threshold value for the split.
            labels (array-like): Corresponding class labels.
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
    def stopping_criteria(features, labels, depth):
        """
        Determine if the tree should stop splitting further.
        Args:
            features (array-like): Feature matrix.
            labels (array-like): Class labels.
            depth (int): Current depth of the tree.
        Returns:
            bool: True if stopping criteria are met, False otherwise.
        """
        if len(np.unique(labels)) <= 1:
            return True
        if depth >= MAX_DEPTH:
            return True
        return False

    def fit(self, features, labels):
        """
        Fit the decision tree to the provided features and labels.
        Args:
            features (array-like): Feature matrix.
            labels (array-like): Class labels.
        """
        root = Node()
        self.root = root
        self.root = self.__build__(self.root, features, labels)

    def __build__(self, node, features, labels, depth=0):
        """
        Recursively build the decision tree.
        Args:
            node (Node): Current node.
            features (array-like): Feature matrix.
            labels (array-like): Class labels.
            depth (int): Current depth in the tree.
        Returns:
            Node: The constructed node (leaf or internal).
        """
        if DecisionTree.stopping_criteria(features, labels, depth):
            # Assign the majority class as the value for the leaf node
            values, counts = np.unique(labels, return_counts=True)
            node.value = values[np.argmax(counts)]
            return node
        threshold, feature_to_split_on, IG = self.determine_threshold(features, labels)
        if IG <= 0.1:
            # If information gain is too low, make this a leaf node
            values, counts = np.unique(labels, return_counts=True)
            node.value = values[np.argmax(counts)]
            node.IG = IG
            return node
        left_feature, right_feature, left_labels, right_labels = self.split(features, feature_to_split_on, threshold, labels)
        if len(left_labels) < MIN_SAMPLES_PER_LEAF or len(right_labels) < MIN_SAMPLES_PER_LEAF:
            # If a split would result in a leaf with too few samples, make this a leaf node
            values, counts = np.unique(labels, return_counts=True)
            node.value = values[np.argmax(counts)]
            node.IG = IG
            return node
        node.feature = feature_to_split_on
        node.threshold = threshold
        node.IG = IG
        left_node = Node()
        right_node = Node()
        node.left = self.__build__(left_node, left_feature, left_labels, depth + 1)
        node.right = self.__build__(right_node, right_feature, right_labels, depth + 1)
        return node

    def __traverse__(self, node, x):
        """
        Traverse the tree to predict the class for a single sample.
        Args:
            node (Node): Current node.
            x (array-like): Feature vector for a single sample.
        Returns:
            Predicted class label.
        """
        if node.is_leaf():
            return node.value
        if x[node.feature] <= node.threshold:
            # Traverse left subtree
            return self.__traverse__(node.left, x)
        else:
            # Traverse right subtree
            return self.__traverse__(node.right, x)

    def predict(self, X):
        """
        Predict class labels for a batch of samples.
        Args:
            X (array-like): Feature matrix.
        Returns:
            list: Predicted class labels for each sample.
        """
        return [self.__traverse__(self.root, X[i]) for i in range(len(X))]

    def predict_one(self, x):
        """
        Predict the class label for a single sample.
        Args:
            x (array-like): Feature vector for a single sample.
        Returns:
            Predicted class label.
        """
        return self.__traverse__(self.root, x)

        
        