
def load_iris_dataset():
    """
    Load the Iris dataset from scikit-learn.

    Returns:
        tuple: (data, target, feature_names, target_names)
            - data (ndarray): Feature matrix of shape (n_samples, n_features)
            - target (ndarray): Array of target class labels
            - feature_names (list): List of feature names
            - target_names (list): List of target class names

    Example:
        X, y, feature_names, target_names = load_iris_dataset()
    """
    from sklearn import datasets  # Import inside function for modularity
    dataset = datasets.load_iris()
    # Return features, labels, and metadata
    return dataset.data, dataset.target, dataset.feature_names, dataset.target_names