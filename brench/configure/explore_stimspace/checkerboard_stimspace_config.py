import time
from pathlib import Path
import numpy as np

from brench.utils.adapters import ODOG_RHS2007
import brench.run
from brench.evaluate import (
    calculate_targets_difference,
    create_RHS_table,
    plot_all_outputs,
    save_plot,
)
from prepare_checkerboards import create_checkerboard_funcs


# If existent, load model outputs:
load_pickle = True
# Save model outputs and evaluation results:
save_pickle = True
# Output dir for all outputs:
output_dir = Path(__file__).parents[3] / "data" / "checkerboard_stimspace"


# Configure models:
models = [
    {
        "name": "ODOG_RHS2007_32deg",
        "adapter": ODOG_RHS2007,
        "params": {
            "model": "ODOG_RHS2007",
            "visextent": (-16.0, 16.0, -16.0, 16.0),
        },
    },
]


# Configure stimuli
# Specify the stimspace that you want to test
board_heights = [15, 31]
board_widths = [15]
check_sizes = [1.]

# Create dictionary of checkerboard functions covering the specified stimspace:
stimuli = create_checkerboard_funcs(board_heights, board_widths, check_sizes)


# Create config dict with models and stimuli
config_dict = {"models": models, "stimuli": stimuli}


# Run framework with specified config and evaluation functions:
def run_config():
    brench.run(
        config_dict,
        evaluate_individual,
        evaluate_all,
        outputs_dir=output_dir,
        save=save_pickle,
        load=load_pickle,
    )


# Define which evaluation steps should be performed for each model individually:
def evaluate_individual(model_name, stimulus_name, model_output, stim, outputs_dir):
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
    create_RHS_table(
        outputs_dir / "diffs",
        outputs_dir / "target_differences.csv",
        normalized=False,
    )
    pass


if __name__ == "__main__":
    start = time.time()
    run_config()
    stop = time.time()

print("All done! Elapsed time: ", np.round(stop - start, 3))
