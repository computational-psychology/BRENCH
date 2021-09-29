# Models
from brench.utils.adapters import domijan2015

# Stimuli
import stimuli.papers.domijan2015 as domijan_stimuli

# Evaluate
from brench.evaluate import (
    calculate_targets_difference,
    create_RHS_table,
    plot_all_outputs,
    save_plot,
)


# Where does this config save, by default?
from pathlib import Path

output_dir = Path(__file__).parents[2] / "data" / "Domijan2015"


# Configure models:
models = [
    {
        "name": "domijan2015",
        "model_func": domijan2015,
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


# Define which evaluation steps should be performed for each model individually:
def evaluate_each(model_name, stimulus_name, model_output, stim, outputs_dir):
    # TODO: add '{model_name}-{stimulus_name}' as default out values in all the evaluation functions

    # Do the target masks exist?
    if stim.target_mask is not None:
        # Save plots for all model outputs individually in subfolder "plots":
        plot_file = outputs_dir / "plots" / f"{model_name}-{stimulus_name}.png"
        save_plot(
            model_output["image"],
            out=plot_file,
        )
        print(f"    saved plot {plot_file}")

        # Calculate and save the difference in estimated target intensity individually in "diffs"
        diff_file = (
            outputs_dir / "diffs" / f"{model_name}-{stimulus_name}.pickle"
        )
        calculate_targets_difference(
            model_output["image"],
            stim.target_mask,
            out=diff_file,
        )
        print(f"    saved target differences to {diff_file}")


# Define which evaluation step should be performed using all model results:
def evaluate_all(outputs_dir):
    """
    This function assumes all values are saved in files with format "{model_name}-{stimulus_name}"
    """
    # Create an overview plot with all model outputs for the different stimuli:
    combined_plots = outputs_dir / "all_model_outputs.png"
    plot_all_outputs(stimuli, outputs_dir / "plots", combined_plots)
    print(f"Saved combined figure as {combined_plots}")

    # Create table with mean target differences for all models and stimuli:
    table_file = outputs_dir / "target_differences.csv"
    create_RHS_table(
        outputs_dir / "diffs",
        table_file,
        normalized=True,
    )
    print(f"Saved table of target differences to {table_file}")


# Run from the command-line
if __name__ == "__main__":
    import time
    import brench.run

    # If existent, load model outputs:
    load_pickle = True
    # Save model outputs and evaluation results:
    save_pickle = True

    start = time.time()

    # Run framework with specified config and evaluation functions:
    brench.run(
        models,
        stimuli,
        evaluate_each,
        evaluate_all,
        outputs_dir=output_dir,
        load=load_pickle,
        save=save_pickle,
    )

    stop = time.time()
    print(
        "All done! Elapsed time:"
        f" {((stop-start)/60):2.0f}m:{((stop-start) % 60):2.0f}s"
    )
