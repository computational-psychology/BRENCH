import brench.run
from brench.utils.adapters import multyscale, domijan2015
from brench.evaluate import (
    calculate_targets_difference,
    create_RHS_table,
    plot_all_outputs,
)
from brench.utils import (
    save_dict,
    load_dict,
)
from adelson_checkershadow import adelson_checkershadow

import stimuli.papers.RHS2007 as RHS_stimuli
import stimuli.papers.domijan2015 as domijan_stimuli


load_pickle = False
save_pickle = False
output_filename = "full_output"

if not load_pickle:
    print("Initialising models...")
    models = [
        {
            "name": "ODOG_RHS2007_32deg",
            "runner": multyscale,
            "model": "ODOG_RHS2007",
            "params": {"visextent": (-16.0, 16.0, -16.0, 16.0)},
        },
        {
            "name": "LODOG_RHS2007_32deg",
            "runner": multyscale,
            "model": "LODOG_RHS2007",
            "params": {"visextent": (-16.0, 16.0, -16.0, 16.0)},
        },
        {
            "name": "FLODOG_RHS2007_32deg",
            "runner": multyscale,
            "model": "FLODOG_RHS2007",
            "params": {"visextent": (-16.0, 16.0, -16.0, 16.0)},
        },
        {
            "name": "ODOG_RHS2007_3.2deg",
            "runner": multyscale,
            "model": "ODOG_RHS2007",
            "params": {"visextent": (-1.6, 1.6, -1.6, 1.6)},
        },
        {
            "name": "FLODOG_RHS2007_3.2deg",
            "runner": multyscale,
            "model": "FLODOG_RHS2007",
            "params": {"visextent": (-1.6, 1.6, -1.6, 1.6)},
        },
        {
            "name": "domijan2015",
            "runner": domijan2015,
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


def run_config():
    if load_pickle:
        res = load_dict(output_filename + ".pickle")
    else:
        res = brench.run(config_dict)
        if save_pickle:
            save_dict(res, output_filename + ".pickle")
    return res


def evaluate(pipeline_dict):
    res = calculate_targets_difference(pipeline_dict)
    plot_all_outputs(res, output_filename=output_filename + ".png")
    table = create_RHS_table(res, "output.csv", normalized=True)
    return table


if __name__ == "__main__":
    import time
    import numpy as np

    start = time.time()
    res = run_config()
    evaluate(res)

    stop = time.time()
    print("All done! Elapsed time: ", np.round(stop - start, 3))
