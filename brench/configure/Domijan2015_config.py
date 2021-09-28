from pathlib import Path
from brench.utils.adapters import domijan2015
import brench.run
from brench.evaluate import (
    calculate_targets_difference,
    # FIXME create_RHS_table,
    plot_all_outputs,
    save_plot,
)

import stimuli.papers.domijan2015 as domijan_stimuli

load_pickle = True
save_pickle = True
output_dir = Path(__file__).parents[2] / "data" / "Domijan2015"


models = [
    {
        "name": "domijan2015",
        "adapter": domijan2015,
        "params": {"S": 20},
    }
]

stimuli = {
    "dungeon": domijan_stimuli.dungeon,
    # "cube": domijan_stimuli.cube,
    # "grating": domijan_stimuli.grating,
    "ring": domijan_stimuli.rings,
    # "bullseye": domijan_stimuli.bullseye,
    # "simultaneous_brightness_contrast": domijan_stimuli.simultaneous_brightness_contrast,
    # "white": domijan_stimuli.white,
    # "benary_cross": domijan_stimuli.benary,
    "todorovic": domijan_stimuli.todorovic,
    # "checkerboard_contrast_contrast": domijan_stimuli.checkerboard_contrast_contrast,
    # "checkerboard_contrast": domijan_stimuli.checkerboard,
    # "checkerboard_contrast_extended": domijan_stimuli.checkerboard_extended,
}

domijan2015_config = {"models": models, "stimuli": stimuli}


def run():
    brench.run(
        domijan2015_config,
        evaluate,
        final,
        outputs_dir=output_dir,
        load=load_pickle,
        save=save_pickle,
    )


def evaluate(model_name, stimulus_name, model_output, stim, outputs_dir):
    # TODO: add '{model_name}-{stimulus_name}' as default out values in all the evaluation functions

    # Do the target masks exist?
    if stim.target_mask is not None:
        # Save plots for all model outputs individually in subfolder "plots":
        save_plot(
            model_output["image"],
            out=outputs_dir / "plots" / f"{model_name}-{stimulus_name}.png",
        )

        # Calculate and save the difference in estimated target intensity individually in "diffs"
        calculate_targets_difference(
            model_output["image"],
            stim.target_mask,
            out=outputs_dir / "diffs" / f"{model_name}-{stimulus_name}.pickle",
        )


def final(outputs_dir):
    """
    This function assumes all values are saved in files with format "{model_name}-{stimulus_name}"
    """
    # Create an overview plot with all model outputs for the different stimuli:
    plot_all_outputs(
        outputs_dir / "plots", outputs_dir / "all_model_outputs.png"
    )

    # Create table with mean target differences for all models and stimuli:
    # TODO: fix bug with "None" target masks (probably when there more than two target mask values)
    #    create_RHS_table(outputs_dir / "diffs", outputs_dir / "target_differences.csv", normalized=True)
    pass


if __name__ == "__main__":
    res = run()
