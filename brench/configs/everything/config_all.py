from weasyprint import HTML
import pickle

from pipeline.adapters.multyscale import main as multyscale_main
from pipeline.adapters.domijan2015 import main as domijan_main

import stimuli.papers.RHS2007 as RHS_stimuli
import stimuli.papers.domijan2015 as domijan_stimuli

from pipeline import main
from pipeline.utils import create_RHS_table, plot_outputs
from pipeline.postprocessing import mean_target_value

import time


print("Initialising models...")
models = [
    {
        "name": "domijan2015",
        "runner": domijan_main,
        "model": None,
        "params": {"S": 20},
    },
    {
        "name": "ODOG_BM1999",
        "runner": multyscale_main,
        "model": "ODOG_BM1999",
        "params": {"visextent": (-16, 16, -16, 16)},
    },
    {
        "name": "LODOG_RHS2007",
        "runner": multyscale_main,
        "model": "LODOG_RHS2007",
        "params": {"visextent": (-16, 16, -16, 16)},
    },
    {
        "name": "FLODOG_RHS2007",
        "runner": multyscale_main,
        "model": "FLODOG_RHS2007",
        "params": {"visextent": (-16, 16, -16, 16)},
    },
]

print("Initialising stimuli...")
stimuli = {
    "RHS2007_WE_thick": RHS_stimuli.WE_thick,
    "RHS2007_WE_thin_wide": RHS_stimuli.WE_thin_wide,
    "RHS2007_WE_dual": RHS_stimuli.WE_dual,
    "RHS2007_WE_anderson": RHS_stimuli.WE_anderson,
    "RHS2007_WE_howe": RHS_stimuli.WE_howe,
    "RHS2007_WE_radial_thick_small": RHS_stimuli.WE_radial_thick_small,
    "RHS2007_WE_radial_thick": RHS_stimuli.WE_radial_thick,
    "RHS2007_WE_radial_thin_small": RHS_stimuli.WE_radial_thin_small,
    "RHS2007_WE_radial_thin": RHS_stimuli.WE_radial_thin,
    "RHS2007_WE_circular1": RHS_stimuli.WE_circular1,
    "RHS2007_WE_circular05": RHS_stimuli.WE_circular05,
    "RHS2007_WE_circular025": RHS_stimuli.WE_circular025,
    "RHS2007_grating_induction": RHS_stimuli.grating_induction,
    "RHS2007_sbc_large": RHS_stimuli.sbc_large,
    "RHS2007_sbc_small": RHS_stimuli.sbc_small,
    "RHS2007_todorovic_equal": RHS_stimuli.todorovic_equal,
    "RHS2007_todorovic_in_large": RHS_stimuli.todorovic_in_large,
    "RHS2007_todorovic_in_small": RHS_stimuli.todorovic_in_small,
    "RHS2007_checkerboard016": RHS_stimuli.checkerboard_016,
    "RHS2007_checkerboard0938": RHS_stimuli.checkerboard_0938,
    "RHS2007_checkerboard209": RHS_stimuli.checkerboard209,
    "domijan2015_dungeon": domijan_stimuli.dungeon,
    "domijan2015_cube": domijan_stimuli.cube,
    "domijan2015_grating": domijan_stimuli.grating,
    "domijan2015_rings": domijan_stimuli.rings,
    "domijan2015_bullseye": domijan_stimuli.bullseye,
    "domijan2015_sbc": domijan_stimuli.simultaneous_brightness_contrast,
    "domijan2015_white": domijan_stimuli.white,
    "domijan2015_benary": domijan_stimuli.benary,
    "domijan2015_todorovic": domijan_stimuli.todorovic,
    "domijan2015_checkerboard_contrast_contrast": domijan_stimuli.checkerboard_contrast_contrast,
    "domijan2015_checkerboard": domijan_stimuli.checkerboard,
    "domijan2015_checkerboard_extended": domijan_stimuli.checkerboard_extended,
}

RHS2007 = {"models": models, "stimuli": stimuli}


def run():
    res = main.run_model(RHS2007)
    res = mean_target_value(res)
    plot_outputs(res)


if __name__ == "__main__":
    run()
