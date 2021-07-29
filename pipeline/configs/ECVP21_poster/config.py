import matplotlib.pyplot as plt
import pickle

from pipeline import main
from pipeline.adapters.multyscale import main as multyscale_main
from pipeline.adapters.domijan2015 import main as domijan_main

from pipeline.visualise_output import create_RHS_table, plot_outputs
from pipeline.postprocessing import calculate_targets_means
from pipeline.utils import save_dict, load_dict

import stimuli.papers.RHS2007 as RHS_stimuli
import stimuli.papers.domijan2015 as domijan_stimuli

load_pickle = False
save_pickle = False
output_filename = "full_output"

if not load_pickle:
    print("Initialising models...")
    models = [
            {
                "name": "ODOG_RHS2007",
                "runner": multyscale_main,
                "model": "ODOG_RHS2007",
                "params": {"visextent": (-16,16,-16,16)}
            },
            {
                "name": "LODOG_RHS2007",
                "runner": multyscale_main,
                "model": "LODOG_RHS2007",
                "params": {"visextent": (-16,16,-16,16)}
            },
            {
                "name": "FLODOG_RHS2007",
                "runner": multyscale_main,
                "model": "FLODOG_RHS2007",
                "params": {"visextent": (-16, 16, -16, 16)}
            },
            {
                "name": "domijan2015",
                "runner": domijan_main,
                "model": None,
                "params": {"S": 20}
            }
        ]

    stimuli = {
            "RHS2007_WE_thick": RHS_stimuli.WE_thick,
            "RHS2007_checkerboard209": RHS_stimuli.checkerboard209,
            "RHS2007_WE_circular1": RHS_stimuli.WE_circular1,
            "RHS2007_todorovic_in_large": RHS_stimuli.todorovic_in_large,
            "RHS2007_sbc_large": RHS_stimuli.sbc_large,

            "domijan2015_white": domijan_stimuli.white,
            "domijan2015_todorovic": domijan_stimuli.todorovic,
            "domijan2015_sbc": domijan_stimuli.simultaneous_brightness_contrast,
            "domijan2015_checkerboard_contrast": domijan_stimuli.checkerboard,
            "domijan2015_dungeon": domijan_stimuli.dungeon,
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
