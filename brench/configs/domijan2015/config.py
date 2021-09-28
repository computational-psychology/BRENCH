from weasyprint import HTML
import pickle

from pipeline.adapters.domijan2015 import main as domijan_main
from pipeline import main
from pipeline.visualise_output import create_RHS_table, plot_outputs
from pipeline.postprocessing import calculate_targets_means
from pipeline.utils import save_dict, load_dict

import stimuli.papers.domijan2015 as domijan_stimuli

load_pickle = False
save_pickle = False
output_filename = "full_output"

if not load_pickle:
    print("Initialising models...")
    models = [
        {
            "name": "domijan2015",
            "runner": domijan_main,
            "model": None,
            "params": {"S": 20},
        }
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
        "checkerboard contrast extended": domijan_stimuli.checkerboard_extended,
    }

domijan2015 = {"models": models, "stimuli": stimuli}


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
