from brench.utils import multyscale
import brench.run
from brench.utils import save_dict, load_dict
from brench.evaluate import (
    calculate_targets_difference,
    create_RHS_table,
    plot_all_outputs,
)

import stimuli.papers.RHS2007 as RHS_stimuli

load_pickle = False
save_pickle = False
output_filename = "full_output"

if not load_pickle:
    print("Initialising models...")
    models = [
        {
            "name": "ODOG_RHS2007",
            "runner": multyscale,
            "model": "ODOG_RHS2007",
            "params": {"visextent": (-16, 16, -16, 16)},
        },
        {
            "name": "LODOG_RHS2007",
            "runner": multyscale,
            "model": "LODOG_RHS2007",
            "params": {"visextent": (-16, 16, -16, 16)},
        },
        {
            "name": "FLODOG_RHS2007",
            "runner": multyscale,
            "model": "FLODOG_RHS2007",
            "params": {"visextent": (-16, 16, -16, 16)},
        },
    ]

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

    RHS2007 = {"models": models, "stimuli": stimuli}


def run():
    if load_pickle:
        res = load_dict(output_filename + ".pickle")
    else:
        res = brench.run(RHS2007)
        if save_pickle:
            save_dict(res, output_filename + ".pickle")
    return res


def evaluate(pipeline_dict):
    res = calculate_targets_difference(pipeline_dict)
    plot_all_outputs(res, output_filename=output_filename + ".png")
    table = create_RHS_table(res, "output.csv", normalized=True)
    return table


if __name__ == "__main__":
    res = run()
    evaluate(res)
