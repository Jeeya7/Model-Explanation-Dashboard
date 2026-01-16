def main():
    
    from models import decision_tree
    from data import loaders
    from sklearn.model_selection import train_test_split
    import numpy as np
    
    tree_model = decision_tree.DecisionTree()
    features, labels, feature_names, label_names = loaders.load_iris_dataset()
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.33, random_state=42)
    tree_model.fit(X_train, y_train)
    preds = tree_model.predict(X_test)

    acc = np.mean(np.array(preds) == np.array(y_test))
    print(acc)

    return
    
if __name__== "__main__":
    main()