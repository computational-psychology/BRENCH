import csv
import matplotlib.pyplot as plt
import matplotlib
from collections import OrderedDict

from pipeline.postprocessing import calculate_RHS_table_values

def size_to_px(size, dpi):
    return (size[0]*dpi[0], size[1]*dpi[1])

def px_to_size(pixel_size, dpi):
    return(pixel_size[0]/dpi, pixel_size[1]/dpi)


def plot_outputs(res, fig_px_size=None, fig_dpi=100, output_filename=None):
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
                plt.imshow(output().img, cmap='gray')
            else:
                plt.imshow(output["image"], cmap='coolwarm')
            plt.colorbar()
    plt.tight_layout()
    if output_filename is not None:
        plt.savefig(output_filename)
    plt.show()



def create_RHS_table(pipeline_dict, output_filename, normalized=True):
    table_values = {}
    for model_name, outputs in pipeline_dict.items():
        if model_name != 'input_stimuli':
            normalization = 1
            if normalized:
                normalization_key = tuple(key for key in pipeline_dict[model_name] if "we_thick" in key.lower())
                normalization = abs(calculate_RHS_table_values(pipeline_dict[model_name][normalization_key[0]]['means'])) if len(normalization_key) else 1
            for stim_name, output in outputs.items():
                if stim_name not in table_values:
                    table_values[stim_name] = OrderedDict()
                table_values[stim_name][model_name] = calculate_RHS_table_values(pipeline_dict[model_name][stim_name]['means'], normalization)

    output_file = open(output_filename, "w")
    csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    models = []
    for model_name in pipeline_dict:
        models.append(model_name)
    csv_writer.writerow(models)

    for stim_name, model_names in table_values.items():
        row = [stim_name]
        for model_name, table_value in model_names.items():
            row.append(round(table_value,2))
        csv_writer.writerow(row)




