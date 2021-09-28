import matplotlib.pyplot as plt
import pickle
import time

from brench import main
from brench.adapters.multyscale import main as multyscale_main
from brench.adapters.domijan2015 import main as domijan_main
from brench.postprocessing import calculate_targets_means
from brench.utils import save_dict, load_dict, create_RHS_table, plot_outputs
from adelson_checkershadow import adelson_checkershadow

import stimuli.papers.RHS2007 as RHS_stimuli
import stimuli.papers.domijan2015 as domijan_stimuli

start = time.time()
load_pickle = False
save_pickle = False
output_filename = "full_output"

if not load_pickle:
    print("Initialising models...")
    models = [
        {
            "name": "ODOG_RHS2007_32deg",
            "runner": multyscale_main,
            "model": "ODOG_RHS2007",
            "params": {"visextent": (-16.0, 16.0, -16.0, 16.0)},
        },
        {
            "name": "LODOG_RHS2007_32deg",
            "runner": multyscale_main,
            "model": "LODOG_RHS2007",
            "params": {"visextent": (-16.0, 16.0, -16.0, 16.0)},
        },
        {
            "name": "FLODOG_RHS2007_32deg",
            "runner": multyscale_main,
            "model": "FLODOG_RHS2007",
            "params": {"visextent": (-16.0, 16.0, -16.0, 16.0)},
        },
        {
            "name": "ODOG_RHS2007_3.2deg",
            "runner": multyscale_main,
            "model": "ODOG_RHS2007",
            "params": {"visextent": (-1.6, 1.6, -1.6, 1.6)},
        },
        {
            "name": "FLODOG_RHS2007_3.2deg",
            "runner": multyscale_main,
            "model": "FLODOG_RHS2007",
            "params": {"visextent": (-1.6, 1.6, -1.6, 1.6)},
        },
        {
            "name": "domijan2015",
            "runner": domijan_main,
            "model": None,
            "params": {"S": 20},
        },
    ]

    stimuli = {
        "RHS2007_sbc_large": RHS_stimuli.sbc_large,
        "RHS2007_checkerboard209": RHS_stimuli.checkerboard209,
        "RHS2007_WE_thick": RHS_stimuli.WE_thick,
        "RHS2007_todorovic_in_large": RHS_stimuli.todorovic_in_large,
        "RHS2007_WE_circular1": RHS_stimuli.WE_circular1,
        "domijan2015_sbc": domijan_stimuli.simultaneous_brightness_contrast,
        "domijan2015_checkerboard_contrast": domijan_stimuli.checkerboard,
        "domijan2015_white": domijan_stimuli.white,
        "domijan2015_todorovic": domijan_stimuli.todorovic,
        "domijan2015_dungeon": domijan_stimuli.dungeon,
        "adelson_checkershadow": adelson_checkershadow,
    }

    config_dict = {"models": models, "stimuli": stimuli}


def run():
    if load_pickle:
        res = load_dict(output_filename + ".pickle")
    else:
        res = main.run_model(config_dict)
        if save_pickle:
            save_dict(res, output_filename + ".pickle")
    return res


def evaluate(pipeline_dict):
    res = calculate_targets_means(pipeline_dict)
    plot_outputs(res, output_filename=output_filename + ".png")
    table = create_RHS_table(res, "output.csv", normalized=True)


if __name__ == "__main__":
    res = run()
    evaluate(res)

stop = time.time()
print("All done! Elapsed time: ", np.round(stop - start, 3))
