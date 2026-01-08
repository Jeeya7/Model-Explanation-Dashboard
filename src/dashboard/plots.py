from data import loaders
import matplotlib.pyplot as plt

def plot_feature_scatter_by_class():
    x, y, feature_column_names, class_labels = loaders.load_iris_dataset()
    
    # Plot
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10,4))
    scatter1 =  ax[0].scatter(x[:,0], x[:,1], c=y)
    ax[0].set(xlabel=feature_column_names[0], ylabel=feature_column_names[1])
    ax[0].legend(scatter1.legend_elements()[0], class_labels, loc="lower right", title="Classes")
    
    scatter2 = ax[1].scatter(x[:,2], x[:,3], c=y)
    ax[1].set(xlabel=feature_column_names[2], ylabel=feature_column_names[3])
    ax[1].legend(scatter2.legend_elements()[0], class_labels, loc="lower right", title="Classes")
    plt.show()
    
    
    