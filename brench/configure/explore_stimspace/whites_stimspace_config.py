import time
from pathlib import Path
import numpy as np

import stimuli.illusions
from brench.utils.adapters import ODOG_RHS2007
import brench.run
from brench.evaluate import (
    calculate_targets_difference,
    create_RHS_table,
    save_plot,
)


load_pickle = True
save_pickle = True
output_dir = Path(__file__).parents[3] / "data" / "whites_stimspace"


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


stimuli_white = {}
grating_frequencies = [0.25, 0.5]
target_heights = [
    0.1,
]
target_luminances = [
    0.5,
]
for freq in grating_frequencies:
    for h in target_heights:
        for lum in target_luminances:
            name = f"white_{freq}_{h}_{lum}"
            total_height, total_width, ppd = (32,) * 3
            height, width = 12, 16
            padding_horizontal = (total_width - width) / 2
            padding_vertical = (total_height - height) / 2
            padding = (
                padding_vertical,
                padding_vertical,
                padding_horizontal,
                padding_horizontal,
            )
            # lambda here is needed because we have to pass a function to the stimuli dictionary instead of an actual stimulus object
            # FIXME: incorrectly produced stimuli...
            stim_func = lambda: stimuli.illusions.whites.white(
                shape=(12, 16),
                ppd=ppd,
                frequency=freq,
                period="ignore",
                target_indices=(2, -3),
                target_height=h * height,
                high=0.9,
                low=0.1,
                target=lum,
                padding=padding,
                padding_val=0.5,
            )
            stimuli_white[name] = stim_func


config_dict = {
    "models": models,
    "stimuli": stimuli_white,
}


def run_config():
    brench.run(
        config_dict,
        evaluate,
        final,
        outputs_dir=output_dir,
        save=save_pickle,
        load=load_pickle,
    )


def evaluate(model_name, stimulus_name, model_output, stim, outputs_dir):
    # TODO: add '{model_name}-{stimulus_name}' as default out values in all the evaluation functions

    # Generally you should check if target mask exists
    # if stim.target_mask is not None:
    #    calculate_targets_difference(model_output['image'], stim.target_mask, out=f"evaluate/diffs/{model_name}-{stimulus_name}.pickle")
    save_plot(
        model_output["image"],
        out=outputs_dir / "plots" / f"{model_name}-{stimulus_name}.png",
    )
    calculate_targets_difference(
        model_output["image"],
        stim.target_mask,
        out=outputs_dir / "diffs" / f"{model_name}-{stimulus_name}.pickle",
    )


def final(outputs_dir):
    """
    This function assumes all values are saved in files with format "{model_name}-{stimulus_name}"
    """
    create_RHS_table(
        outputs_dir / "diffs",
        outputs_dir / "target_differences.csv",
        normalized=False,
    )
    # plot_all_outputs("evaluate/plots", "all.png")
    pass


if __name__ == "__main__":
    start = time.time()
    run_config()
    stop = time.time()

print("All done! Elapsed time: ", np.round(stop - start, 3))
