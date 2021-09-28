from pathlib import Path
import brench.run
from brench.utils.adapters import ODOG_RHS2007, LODOG_RHS2007, FLODOG_RHS2007
from brench.evaluate import (
    calculate_targets_difference,
    create_RHS_table,
    plot_all_outputs,
    save_plot
)

import stimuli.papers.RHS2007 as RHS_stimuli

load_pickle = True
save_pickle = True
output_dir = Path(__file__).parents[2] / "data" / "RHS2007"


# Configure models:
models = [
    {
        "name": "ODOG_RHS2007",
        "adapter": ODOG_RHS2007,
        "params": {"visextent": (-16, 16, -16, 16)},
    },
    {
        "name": "LODOG_RHS2007",
        "adapter": LODOG_RHS2007,
        "params": {"visextent": (-16, 16, -16, 16)},
    },
    {
        "name": "FLODOG_RHS2007",
        "adapter": FLODOG_RHS2007,
        "params": {"visextent": (-16, 16, -16, 16)},
    },
]


# Configure stimuli
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


# Create config dict from models and stimuli
RHS2007_config = {"models": models, "stimuli": stimuli}


def run():
    brench.run(
        RHS2007_config,
        evaluate,
        final,
        outputs_dir=output_dir,
        load=load_pickle,
        save=save_pickle,
    )


# Define which evaluation steps should be performed:
def evaluate(model_name, stimulus_name, model_output, stim, outputs_dir):
    # TODO: add '{model_name}-{stimulus_name}' as default out values in all the evaluation functions

    # Do the target masks exist?
    if stim.target_mask is not None:
        # Save plots for all model outputs individually in subfolder "plots":
        save_plot(
            model_output["image"],
            out=f"evaluate/plots/{model_name}-{stimulus_name}.png",
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
