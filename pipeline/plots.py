import matplotlib.pyplot as plt
import matplotlib


def size_to_px(size, dpi):
    return (size[0]*dpi[0], size[1]*dpi[1])

def px_to_size(pixel_size, dpi):
    return(pixel_size[0]/dpi, pixel_size[1]/dpi)


def plot_outputs(res, fig_px_size=None, fig_dpi=100):
    """
    fig_px_size: int tuple (width, height) specifying figure size in pixels

    """

    rows = len(res)
    cols = len(list(res.values())[0])

    if fig_px_size is not None:
        fig_width, fig_height = px_to_size(fig_px_size, fig_dpi)
    else:
        fig_height, fig_width = (3*rows, 4*cols)

    plt.figure(figsize=[fig_width, fig_height], dpi=fig_dpi)
    plt.subplots_adjust(left=0.05, right=0.95)
    matplotlib.rcParams.update({'font.size': 12})

    for i, (model_name, model_output) in enumerate(res.items()): # i = row index
        for j, (stimulus, output) in enumerate(model_output.items()): # j = col index
            index = i*cols + j + 1
            plt.subplot(rows, cols, index)
            plt.title(model_name + "\n" + stimulus)
            if model_name == "input_stimuli":
                plt.imshow(output, cmap='gray')
            else:
                plt.imshow(output["image"], cmap='coolwarm')
            plt.colorbar()
    plt.show()