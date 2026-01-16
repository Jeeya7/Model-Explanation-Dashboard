import numpy as np
import pandas as pd

# Hyperparameters 
MAX_DEPTH = 3
MIN_SAMPLES_PER_LEAF = 2

class Node:
    
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None, IG=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value 
        self.IG = IG
    
    def is_leaf(self):
        if(self.value is not None):
            return True
        else:
            return False
    
    
class DecisionTree:

    def __init__(self, root=None):
        self.root = root # the starting point of the tree
        
        
    def calculate_entropy(self, features):
        
        if len(features) == 0:
            return 0
        y_series = pd.Series(features)
        value_counts = y_series.value_counts()
        
        prob = value_counts/len(features)
        log_p = []
        for i in range(len(prob)):
            log_p.append(np.log(prob.iloc[i]))
        
        prob = np.array(prob)
        log_p = np.array(log_p)
        
        prod = prob * log_p * -1
        
        entropy = prod.sum()

        return entropy
    
    
    def determine_threshold(self, features, labels):
                  
        dataset_entropy = self.calculate_entropy(labels)
        IG = []
        thresholds = []
        features = np.array(features)
        for feature in range(len(features[0])):
            features_sorted = np.sort(features[:,feature])
            features_unique = np.unique(features_sorted)
            feature_thresholds = []
            IG_per_feature = []
            for i in range(len(features_unique) - 1):
                
                left, right = features_unique[i], features_unique[i+1]
                
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
        
        if (len(np.unique(labels)) <= 1):
            return True
        
        if (depth >= MAX_DEPTH):
            return True

        else:
            return False
        
        
    def fit(self, features, labels):
        root = Node()
        self.root = root
        self.root = self.__build__(self.root, features, labels)
        
        

    def __build__(self, node, features, labels, depth=0):
        
        if DecisionTree.stopping_criteria(features, labels, depth):
            
            # majority vote
            values, counts = np.unique(labels, return_counts=True)
            node.value = values[np.argmax(counts)]

            return node
        
        threshold, feature_to_split_on, IG = self.determine_threshold(features, labels)
        
        if IG <= 0.1:
            values, counts = np.unique(labels, return_counts=True)
            node.value = values[np.argmax(counts)]
            node.IG = IG
            return node

        
        left_feature, right_feature, left_labels, right_labels = self.split(features, feature_to_split_on, threshold, labels)
       
        if len(left_labels) < MIN_SAMPLES_PER_LEAF or len(right_labels) < MIN_SAMPLES_PER_LEAF:

            values, counts = np.unique(labels, return_counts=True)
            node.value = values[np.argmax(counts)]
            node.IG = IG
            return node
        
        node.feature=feature_to_split_on
        node.threshold=threshold
        node.IG = IG
        
        left_node = Node()
        right_node = Node()
        node.left = self.__build__(left_node, left_feature, left_labels, depth + 1)
        node.right = self.__build__(right_node, right_feature, right_labels, depth + 1)
                
        return node
    
    def __traverse__(self, node, x):
        
        if node.is_leaf():
            return node.value
        
        if x[node.feature] <= node.threshold:
            # Traverse left
            return self.__traverse__(node.left, x)

        else:
            # Traverse Right
            return self.__traverse__(node.right, x)
                
    def predict(self, X):
        return[self.__traverse__(self.root, X[i]) for i in range(len(X))]
    
    def predict_one(self, x):
        return self.__traverse__(self.root, x)

        
        