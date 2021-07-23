from weasyprint import HTML
import pickle

from pipeline.adapters.multyscale import main as multyscale_main
from pipeline import main
from pipeline.visualise_output import create_RHS_table, plot_outputs
from pipeline.postprocessing import calculate_targets_means
from pipeline.utils import save_dict, load_dict

import stimuli.papers.domijan2015 as domijan_stimuli

load = False

if not load:
    print("Initialising models...")
    models = [
            {
                "name": "ODOG_RHS2007",
                "runner": multyscale_main,
                "model": "ODOG_RHS2007",
                "params": {"visextent": (-16,16,-16,16)}
            },
            # {
            #     "name": "LODOG_RHS2007",
            #     "runner": multyscale_main,
            #     "model": "LODOG_RHS2007",
            #     "params": {"visextent": (-16,16,-16,16)}
            # },
            # {
            #     "name": "FLODOG_RHS2007",
            #     "runner": multyscale_main,
            #     "model": "FLODOG_RHS2007",
            #     "params": {"visextent": (-16, 16, -16, 16)}
            # }
        ]

    print("Initialising stimuli...")
    stimuli = {
        "dungeon": domijan_stimuli.dungeon,
        "cube": domijan_stimuli.cube,
        "grating": domijan_stimuli.grating,
        "ring": domijan_stimuli.rings,
        "bullseye": domijan_stimuli.bullseye,
        "simultaneous brightness contrast": domijan_stimuli.simultaneous_brightness_contrast,
        "white": domijan_stimuli.white,
        "benary_cross": domijan_stimuli.benary,
        "todorovic": domijan_stimuli.todorovic,
        "checkerboard contrast-contrast": domijan_stimuli.checkerboard_contrast_contrast,
        "checkerboard contrast": domijan_stimuli.checkerboard,
        "checkerboard contrast extended": domijan_stimuli.checkerboard_extended
        }

    RHS2007 = {"models": models, "stimuli": stimuli}


def run():
    if load:
        res = load_dict("output_ODOG.pickle")
    else:
        res = main.run_model(RHS2007)
        save_dict(res, "output_ODOG.pickle")

    res = calculate_targets_means(res)
    plot_outputs(res)
    table = create_RHS_table(res)
    html = HTML(string=table)
    html.write_pdf("output_ODOG.pdf")

if __name__ == "__main__":
    run()
