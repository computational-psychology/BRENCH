import os
from brench.adapters.domijan2015 import main as domijan_main
from brench import main
from brench.postprocessing import (
    calculate_targets_difference,
    create_RHS_table,
    plot_all_outputs,
    save_plot,
    save_output
)
#from brench.utils import save_dict, load_dict

import stimuli.papers.domijan2015 as domijan_stimuli

load_pickle = False
save_pickle = False
output_filename = "full_output"

if not load_pickle:
    print("Initialising models...")
    models = [
        {
            "name": "domijan2015",
            "adapter": domijan_main,
            "model": None,
            "params": {"S": 20},
        }
    ]

    print("Initialising stimuli...")
    stimuli = {
        "dungeon": domijan_stimuli.dungeon,
        "cube": domijan_stimuli.cube,
        "grating": domijan_stimuli.grating,
        "ring": domijan_stimuli.rings,
        "bullseye": domijan_stimuli.bullseye,
        "simultaneous_brightness_contrast": domijan_stimuli.simultaneous_brightness_contrast,
        "white": domijan_stimuli.white,
        "benary_cross": domijan_stimuli.benary,
        "todorovic": domijan_stimuli.todorovic,
        "checkerboard_contrast_contrast": domijan_stimuli.checkerboard_contrast_contrast,
        "checkerboard_contrast": domijan_stimuli.checkerboard,
        "checkerboard_contrast_extended": domijan_stimuli.checkerboard_extended,
    }

domijan2015 = {"models": models, "stimuli": stimuli}


def run():
    main.main(domijan2015, evaluate, final, os.path.join("evaluate", "outputs"))


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
#    create_RHS_table("evaluate/diffs", "output.csv", normalized=True)
    pass


if __name__ == "__main__":
    res = run()
