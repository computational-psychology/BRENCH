import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
import csv


from brench import utils


def generate_js_data():
    """
    This function should be run in the final() step.
    It should take the outputs of the model and 'convert' them
    to a js file/data that can be read by the browser visualisation
    """
    pass


def calculate_targets_difference(
    output_image,
    target_mask,
    out,
    mode="median",
):
    """
    out: path to the output file
    """
    head, tails = os.path.split(out)
    if not os.path.isdir(head):
        os.makedirs(head)
    masked_outputs = get_all_masked_values(output_image, target_mask)
    means = {}
    for i, masked_output in enumerate(masked_outputs):
        if mode == "median":
            means[i + 1] = np.median(masked_output[masked_output.nonzero()])
        elif mode == "mean":
            means[i + 1] = np.mean(masked_output[masked_output.nonzero()])
        else:
            raise ValueError("mode needs to be either 'median' or 'mean'")

    utils.save_dict(means, out)

    return means


def get_all_masked_values(img, mask):
    imgs = []
    for i in range(1, int(mask.max()) + 1):
        m = mask == i
        imgs.append(get_masked_values(img, m))
    return imgs


def get_masked_values(img, mask):
    mask = mask.astype(bool)
    new_img = np.zeros(img.shape)
    new_img[mask] = img[mask]

    return new_img


def calculate_RHS_table_values(means_dict, normalization=None):
    n = len(means_dict)
    if normalization is None:
        normalization = 1

    if n == 2:
        patch1 = means_dict[1]
        patch2 = means_dict[2]
        return (patch1 - patch2) / normalization
    else:
        # TODO: handle cases with n>2
        return "None"


def sort_target_patches(means_dict):
    return sorted(means_dict.items(), key=lambda kv: kv[1])


def save_plot(stim, output_image, out):
    # TODO: add option to save colorbar
    head, tails = os.path.split(out)
    if not os.path.isdir(head) and head != "":
        os.makedirs(head)
    # Calculate abs max for symmetric colorcoding around 0:
    abs_max = np.abs(output_image).max()
    # Plot input stimulus:
    plt.figure(figsize=(12, 8))
    plt.subplot(1, 2, 1)
    # Plot model output:
    plt.imshow(stim.img, cmap='gray')
    plt.subplot(1, 2, 2)
    plt.imshow(output_image, vmin=-abs_max, vmax=abs_max, cmap="coolwarm")
    plt.savefig(out)
    plt.close()


def plot_all_outputs(stimuli, input_dir, out, fig_px_size=None, fig_dpi=100):
    """
    fig_px_size: int tuple (width, height) specifying figure size in pixels
    """
    full_dict = {}
    list_stim_names = []
    for filename in os.listdir(input_dir):
        model_name, stim_name = filename.split("-")
        # Create a list with all stim_names for plotting them later:
        if stim_name not in list_stim_names:
            list_stim_names.append(stim_name)
        if model_name not in full_dict:
            full_dict[model_name] = {}
        full_dict[model_name][stim_name] = plt.imread(
            os.path.join(input_dir, filename)
        )

    rows = len(full_dict) + 1
    cols = len(list(full_dict.values())[0])

    if fig_px_size is not None:
        fig_width, fig_height = utils.px_to_size(fig_px_size, fig_dpi)
    else:
        fig_height, fig_width = (3 * rows, 4 * cols)

    plt.figure(figsize=[fig_width, fig_height], dpi=fig_dpi)
    plt.subplots_adjust(left=0.05, right=0.95)
    matplotlib.rcParams.update({"font.size": 12})

    for j in range(cols):
        stim_name = list_stim_names[j]
        plt.subplot(rows, cols, j+1)
        plt.title(stim_name[0:-4])
        plt.imshow(stimuli[stim_name[0:-4]]().img, cmap="gray")
        plt.colorbar()

    for i, (model_name, model_outputs) in enumerate(
        full_dict.items()
    ):  # i = row index
        for j, (stim_name, output_image) in enumerate(
            model_outputs.items()
        ):  # j = col index
            index = (i+1) * cols + j + 1
            plt.subplot(rows, cols, index)
            plt.title(model_name + "\n" + stim_name[0:-4])
            plt.imshow(output_image, cmap="coolwarm")
            plt.colorbar()
    plt.tight_layout()

    head, tails = os.path.split(out)
    if not os.path.isdir(head) and head != "":
        os.makedirs(head)
    plt.savefig(out)
    plt.close()


def create_RHS_table(input_dir, out, normalized=True):
    """
    TODO: needs to be checked and tested with the new setup of the pipeline
    """
    table_values = {}
    full_dict = {}
    for filename in os.listdir(input_dir):
        model_name, stim_name = filename.split("-")
        means = utils.load_dict(os.path.join(input_dir, filename))
        if model_name not in full_dict:
            full_dict[model_name] = {}
        full_dict[model_name][stim_name] = means

    for model_name, outputs in full_dict.items():
        normalization = 1
        if normalized:
            normalization_key = tuple(
                key
                for key in full_dict[model_name]
                if "we_thick" in key.lower()
            )
            normalization = (
                abs(
                    calculate_RHS_table_values(
                        full_dict[model_name][normalization_key[0]]
                    )
                )
                if len(normalization_key)
                else 1
            )
        for stim_name, means in outputs.items():
            if stim_name not in table_values:
                table_values[stim_name] = {}
            table_values[stim_name][model_name] = calculate_RHS_table_values(
                full_dict[model_name][stim_name], normalization
            )

    head, tails = os.path.split(out)
    if not os.path.isdir(head) and head != "":
        os.makedirs(head)
    output_file = open(out, "w")
    csv_writer = csv.writer(
        output_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
    )

    headers = ["stimulus"]
    for model_name in full_dict:
        headers.append(model_name)
    csv_writer.writerow(headers)

    for stim_name, model_names in table_values.items():
        row = [stim_name]
        for model_name, table_value in model_names.items():
            row.append(round(table_value, 2))
        csv_writer.writerow(row)
