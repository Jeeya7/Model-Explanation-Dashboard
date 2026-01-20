from backend.models.decision_tree import DecisionTree as tree
from backend.dashboard.tree_exporter import export_tree
from backend.data import loaders
from sklearn.model_selection import train_test_split
import numpy as np

def tree_service():
    
    # Initialize the custom Decision Tree model
    tree_model = tree()

    # Load the Iris dataset
    features, labels, feature_names, label_names = loaders.load_iris_dataset()

    # Split the data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.33, random_state=42)

    # Train the model
    tree_model.fit(X_train, y_train)
    
    # Make predictions on the test set
    preds = tree_model.predict(X_test)
    
    # Calculate and print accuracy
    acc = np.mean(np.array(preds) == np.array(y_test))
    
    result =  export_tree(tree_model,
                feature_names,
                label_names)
    
    return(result.to_dict())