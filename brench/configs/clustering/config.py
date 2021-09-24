import matplotlib.pyplot as plt
import pickle
import time
import os
import numpy as np

from brench.adapters.multyscale import main as multyscale_main
from brench.adapters.domijan2015 import main as domijan_main
from brench.postprocessing import calculate_targets_difference, create_RHS_table, plot_all_outputs, save_plot, save_output
from brench.utils import save_dict, load_dict
from brench.main import main

import stimuli
import stimuli.papers.RHS2007 as RHS_stimuli
import stimuli.papers.domijan2015 as domijan_stimuli

print("Initialising models...")
models = [
    {
        "name": "ODOG_RHS2007_32deg",
        "adapter": multyscale_main,
        "params": {"model": "ODOG_RHS2007", "visextent": (-16.0, 16.0, -16.0, 16.0)},
    },
]


stimuli_white = {}
grating_frequencies = [0.25,]
target_heights = [0.1,]
target_luminances = [0.0, 0.1,]
for freq in grating_frequencies:
    for h in target_heights:
        for lum in target_luminances:
            name = f"white-{freq}-{h}-{lum}"
            total_height, total_width, ppd = (32,) * 3
            height, width = 12, 16
            padding_horizontal = (total_width - width) / 2
            padding_vertical = (total_height - height) / 2
            padding = (padding_vertical, padding_vertical, padding_horizontal, padding_horizontal)
            #lambda here is needed because we have to pass a function to the stimuli dictionary instead of an actual stimulus object
            stim_func = lambda : stimuli.illusions.whites.white(shape=(12, 16), ppd=ppd, frequency=freq, period='ignore', target_indices=(2, -3), target_height=h * height, high=0.9, low=0.1, target=lum, padding=padding, padding_val=0.5)
            stimuli_white[name] = stim_func

stimuli_checkerboard = {}
check_sizes = (0.05,)
board_widths = (11, )
board_heights = (11, 21,)
extended_targets = (False, True)

def prepare_checkerboard_stim(stim_func):
    stim = stim_func()
    stim.img = stimuli.utils.pad_img_to_shape(stim.img, (1024, 1024), val=0.5)
    stim.target_mask = stimuli.utils.pad_img_to_shape(stim.target_mask, (1024, 1024), val=0.0)
    return stim

for extend in extended_targets:
    for height_checks in board_heights:
        for width_checks in board_widths:
            for check_size in check_sizes:
                name = f"checkerboard-{height_checks}-{width_checks}-{check_size}-{extend}"

                total_height, total_width, ppd = (32,) * 3
                board_shape = (height_checks, width_checks)
                check1, check2, target = 1, 0, .5
                target_height = height_checks // 2
                stim_func = lambda: stimuli.illusions.checkerboard_contrast(ppd=ppd, board_shape=board_shape, check_size=check_size, targets_coords=((target_height, 5), (target_height, -5)),
                                                               extend_targets=extend, check1=check1, check2=check2, target=target)

                # Not totally sure this works, needs to be tested
                stimuli_checkerboard[name] = lambda: prepare_checkerboard_stim(stim_func)


config_dict = {"models": models, "stimuli": {**stimuli_white, **stimuli_checkerboard}}


def run():
    main(config_dict, evaluate, final, os.path.join("evaluate", "outputs"))


def evaluate(model_name, stimulus_name, model_output, stim):
    #TODO: add '{model_name}-{stimulus_name}' as default out values in all the evaluation functions

    # Generally you should check if target mask exists
    #if stim.target_mask is not None:
    #    calculate_targets_difference(model_output['image'], stim.target_mask, out=f"evaluate/diffs/{model_name}-{stimulus_name}.pickle")
    save_plot(model_output['image'], out=f"evaluate/plots/{model_name}-{stimulus_name}.png")
    if "white" in stimulus_name:
        save_output({'model_output': model_output, 'stim': stim}, f"evaluate/outputs/white/{model_name}-{stimulus_name}.pickle")
        calculate_targets_difference(model_output['image'], stim.target_mask, out=f"evaluate/diffs/white/{model_name}-{stimulus_name}.pickle")
    else:
        #TODO: split into checkerboard extended and checkerboard non-extended
        save_output({'model_output': model_output, 'stim': stim}, f"evaluate/outputs/checkerboard/{model_name}-{stimulus_name}.pickle")
        calculate_targets_difference(model_output['image'], stim.target_mask, out=f"evaluate/diffs/checkerboard/{model_name}-{stimulus_name}.pickle")



def final():
    """
        This function assumes all values are saved in files with format "{model_name}-{stimulus_name}"
    """
    #create_RHS_table("evaluate/diffs", "output.csv", normalized=True)
    #plot_all_outputs("evaluate/plots", "all.png")
    pass


if __name__ == "__main__":
    start = time.time()
    run()
    stop = time.time()

print('All done! Elapsed time: ', np.round(stop-start, 3))
