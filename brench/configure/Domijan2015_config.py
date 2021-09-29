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

# If existent, load model outputs:
load_pickle = True
# Save model outputs and evaluation results:
save_pickle = True
# Output dir for all outputs:
output_dir = Path(__file__).parents[2] / "data" / "Domijan2015"


# Configure models:
models = [
    {
        "name": "domijan2015",
        "adapter": domijan2015,
        "params": {"S": 20},
    }
]


# Configure stimuli
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


# Run framework with specified config and evaluation functions:
def run():
    brench.run(
        models,
        stimuli,
        evaluate_individual,
        evaluate_all,
        outputs_dir=output_dir,
        load=load_pickle,
        save=save_pickle,
    )


# Define which evaluation steps should be performed for each model individually:
def evaluate_individual(
    model_name, stimulus_name, model_output, stim, outputs_dir
):
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


# Define which evaluation step should be performed using all model results:
def evaluate_all(outputs_dir):
    """
    This function assumes all values are saved in files with format "{model_name}-{stimulus_name}"
    """
    # Create an overview plot with all model outputs for the different stimuli:
    plot_all_outputs(
        outputs_dir / "plots", outputs_dir / "all_model_outputs.png"
    )

    # Create table with mean target differences for all models and stimuli:
    # TODO: fix bug with "None" target masks (probably when there more than two target mask values)
#    create_RHS_table(
#        outputs_dir / "diffs",
#        outputs_dir / "target_differences.csv",
#        normalized=False,
#    )
    pass


if __name__ == "__main__":
    res = run()
