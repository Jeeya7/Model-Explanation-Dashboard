def load_iris_dataset():
    from sklearn import datasets
    dataset = datasets.load_iris()
    return dataset.data, dataset.target, dataset.feature_names, dataset.target_names