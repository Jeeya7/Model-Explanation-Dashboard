"""
main.py
--------
Entry point for the Model Explanation Dashboard demo.
Trains and evaluates a custom Decision Tree classifier on the Iris dataset.
"""

def main():
    """
    Main execution function for the dashboard demo.
    Loads the Iris dataset, trains a custom Decision Tree, and prints accuracy on the test set.
    """
    # Import custom and third-party modules
    from backend.models import decision_tree
    from backend.data import loaders
    from sklearn.model_selection import train_test_split
    from backend.dashboard.tree_exporter import export_tree
    import numpy as np
    from sklearn import metrics

    # Initialize the custom Decision Tree model
    tree_model = decision_tree.DecisionTree()

    # Load the Iris dataset
    features, labels, feature_names, label_names = loaders.load_iris_dataset()

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.33, random_state=42)

    # Train the model
    tree_model.fit(X_train, y_train)

    # Make predictions on the test set
    preds = tree_model.predict(X_test)
    
    # Calculate the confusion matrix
    conf_matrix = metrics.confusion_matrix(y_pred=preds,
                                           y_true=y_test,
                                           labels=np.unique(labels))
    
    print(conf_matrix)
    # Set metadata for confusion matrix
    confusion_matrix_meta = {
    "orientation": "rows=actual,cols=predicted",
    "normalized": False
    }

    # Calculate and print accuracy
    acc = np.mean(np.array(preds) == np.array(y_test))
    print(f"Test Accuracy: {acc:.4f}")

    resp = export_tree(tree_model, 
                       feature_names, 
                       label_names,
                       conf_matrix,
                       confusion_matrix_meta)

    print(resp.to_dict())
# Entry point for script execution
if __name__ == "__main__":
    main()