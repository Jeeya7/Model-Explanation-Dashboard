from data import loaders
import matplotlib.pyplot as plt

def plot_feature_scatter_by_class():
    data, target, feature_names, target_names = loaders.load_iris_dataset()
    
    # Plot
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10,4))
    scatter1 =  ax[0].scatter(data[:,0], data[:,1], c=target)
    ax[0].set(xlabel=feature_names[0], ylabel=feature_names[1])
    ax[0].legend(scatter1.legend_elements()[0], target_names, loc="lower right", title="Classes")
    
    scatter2 = ax[1].scatter(data[:,2], data[:,3], c=target)
    ax[1].set(xlabel=feature_names[2], ylabel=feature_names[3])
    ax[1].legend(scatter2.legend_elements()[0], target_names, loc="lower right", title="Classes")
    plt.show()
    
    
    