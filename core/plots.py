import matplotlib.pyplot as plt
import matplotlib

def plot_outputs(res):
    M = len(res)
    N = len(list(res.values())[0])

    plt.figure(figsize=[M*6, N*6])


    matplotlib.rcParams.update({'font.size': 14})

    for i, (model_name, model_output) in enumerate(res.items()):
        for j, (stimulus, output) in enumerate(model_output.items()):
            index = i+j*M+1
            plt.subplot(N, M, index)
            plt.title(model_name + " - " + stimulus)
            plt.imshow(output["image"], cmap='coolwarm')
            plt.colorbar()
    plt.show()