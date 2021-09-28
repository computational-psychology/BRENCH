import os
import brench.run
#from brench.utils import save_dict, load_dict
from brench.utils.adapters import multyscale
from brench.evaluate import (
    calculate_targets_difference,
    create_RHS_table,
    plot_all_outputs,
    save_output,
    save_plot
)

import stimuli.papers.RHS2007 as RHS_stimuli

load_pickle = False
save_pickle = False
output_filename = "full_output"

if not load_pickle:
    print("Initialising models...")
    models = [
        {
            "name": "ODOG_RHS2007",
            "adapter": multyscale,
            "model": "ODOG_RHS2007",
            "params": {"visextent": (-16, 16, -16, 16)},
        },
        {
            "name": "LODOG_RHS2007",
            "adapter": multyscale,
            "model": "LODOG_RHS2007",
            "params": {"visextent": (-16, 16, -16, 16)},
        },
        {
            "name": "FLODOG_RHS2007",
            "adapter": multyscale,
            "model": "FLODOG_RHS2007",
            "params": {"visextent": (-16, 16, -16, 16)},
        },
    ]

    stimuli = {
        "WE_thick": RHS_stimuli.WE_thick,
        "WE_thin_wide": RHS_stimuli.WE_thin_wide,
        "WE_dual": RHS_stimuli.WE_dual,
        "WE_anderson": RHS_stimuli.WE_anderson,
        "WE_howe": RHS_stimuli.WE_howe,
        "WE_radial_thick_small": RHS_stimuli.WE_radial_thick_small,
        "WE_radial_thick": RHS_stimuli.WE_radial_thick,
        "WE_radial_thin_small": RHS_stimuli.WE_radial_thin_small,
        "WE_radial_thin": RHS_stimuli.WE_radial_thin,
        "WE_circular1": RHS_stimuli.WE_circular1,
        "WE_circular05": RHS_stimuli.WE_circular05,
        "WE_circular025": RHS_stimuli.WE_circular025,
        "grating_induction": RHS_stimuli.grating_induction,
        "sbc_large": RHS_stimuli.sbc_large,
        "sbc_small": RHS_stimuli.sbc_small,
        "todorovic_equal": RHS_stimuli.todorovic_equal,
        "todorovic_in_large": RHS_stimuli.todorovic_in_large,
        "todorovic_in_small": RHS_stimuli.todorovic_in_small,
        "checkerboard016": RHS_stimuli.checkerboard_016,
        "checkerboard0938": RHS_stimuli.checkerboard_0938,
        "checkerboard209": RHS_stimuli.checkerboard209,
    }

    RHS2007 = {"models": models, "stimuli": stimuli}


def run():
    brench.run(
        RHS2007, evaluate, final, os.path.join("evaluate", "outputs")
    )


def evaluate(model_name, stimulus_name, model_output, stim):
    # TODO: add '{model_name}-{stimulus_name}' as default out values in all the evaluation functions

    # Do the target masks exist?
    if stim.target_mask is not None:
        # Save plots for all model outputs individually in subfolder "plots":
        save_plot(
            model_output["image"],
            out=f"evaluate/plots/{model_name}-{stimulus_name}.png",
        )

        # Save all model outputs individually in subfolder "outputs"
        save_output(
            {"model_output": model_output, "stim": stim},
            f"evaluate/outputs/{model_name}-{stimulus_name}.pickle",
        )

        # Calculate and save the difference in estimated target intensity individually in "diffs"
        calculate_targets_difference(
            model_output["image"],
            stim.target_mask,
            out=f"evaluate/diffs/{model_name}-{stimulus_name}.pickle",
        )


def final():
    """
    This function assumes all values are saved in files with format "{model_name}-{stimulus_name}"
    """
    # Create an overview plot with all model outputs for the different stimuli:
    plot_all_outputs("evaluate/plots", "all.png")

    # Create table with mean target differences for all models and stimuli:
    # TODO: fix bug with "None" target masks (probably when there more than two target mask values)
    create_RHS_table("evaluate/diffs", "output.csv", normalized=True)
    pass


if __name__ == "__main__":
    res = run()
