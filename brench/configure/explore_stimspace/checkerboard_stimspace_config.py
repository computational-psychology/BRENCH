import time
from pathlib import Path
import numpy as np

import stimuli.illusions
from brench.utils.adapters import ODOG_RHS2007
import brench.run
from brench.evaluate import (
    calculate_targets_difference,
    save_plot,
)


load_pickle = True
save_pickle = True
output_dir = Path(__file__).parents[3] / "data" / "checkerboard_stimspace"


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


stimuli_checkerboard = {}
check_sizes = (0.05,)
board_widths = (11,)
board_heights = (
    11,
    21,
)
extended_targets = (False, True)


def prepare_checkerboard_stim(stim_func):
    stim = stim_func()
    stim.img = stimuli.utils.pad_img_to_shape(stim.img, (1024, 1024), val=0.5)
    stim.target_mask = stimuli.utils.pad_img_to_shape(
        stim.target_mask, (1024, 1024), val=0.0
    )
    return stim


for extend in extended_targets:
    for height_checks in board_heights:
        for width_checks in board_widths:
            for check_size in check_sizes:
                name = f"checkerboard-{height_checks}-{width_checks}-{check_size}-{extend}"

                total_height, total_width, ppd = (32,) * 3
                board_shape = (height_checks, width_checks)
                check1, check2, target = 1, 0, 0.5
                target_height = height_checks // 2
                stim_func = lambda: stimuli.illusions.checkerboard_contrast(
                    ppd=ppd,
                    board_shape=board_shape,
                    check_size=check_size,
                    targets_coords=((target_height, 5), (target_height, -5)),
                    extend_targets=extend,
                    check1=check1,
                    check2=check2,
                    target=target,
                )

                # FIXME Not totally sure this works, needs to be tested
                stimuli_checkerboard[name] = lambda: prepare_checkerboard_stim(
                    stim_func
                )


config_dict = {
    "models": models,
    "stimuli": stimuli_checkerboard,
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

    # TODO: split into checkerboard extended and checkerboard non-extended
    calculate_targets_difference(
        model_output["image"],
        stim.target_mask,
        out=outputs_dir / "diffs" / f"{model_name}-{stimulus_name}.pickle",
    )


def final(outputs_dir):
    """
    This function assumes all values are saved in files with format "{model_name}-{stimulus_name}"
    """
    # create_RHS_table("evaluate/diffs", "output.csv", normalized=True)
    # plot_all_outputs("evaluate/plots", "all.png")
    pass


if __name__ == "__main__":
    start = time.time()
    run_config()
    stop = time.time()

print("All done! Elapsed time: ", np.round(stop - start, 3))
