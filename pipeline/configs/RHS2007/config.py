from weasyprint import HTML
import pickle

from pipeline.adapters.multyscale import main as multyscale_main
from pipeline import main
from pipeline.visualise_output import create_RHS_table, plot_outputs
from pipeline.postprocessing import calculate_targets_means
from pipeline.utils import save_dict, load_dict

import stimuli.papers.RHS2007 as RHS_stimuli

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
            # "WE_thick": RHS_stimuli.WE_thick,
            # "WE_thin_wide": RHS_stimuli.WE_thin_wide,
            # "WE_dual": RHS_stimuli.WE_dual,
            # "WE_anderson": RHS_stimuli.WE_anderson,
            # "WE_howe": RHS_stimuli.WE_howe,
            # "WE_radial_thick_small": RHS_stimuli.WE_radial_thick_small,
            # "WE_radial_thick": RHS_stimuli.WE_radial_thick,
            # "WE_radial_thin_small": RHS_stimuli.WE_radial_thin_small,
            # "WE_radial_thin": RHS_stimuli.WE_radial_thin,
            # "WE_circular1": RHS_stimuli.WE_circular1,
            # "WE_circular05": RHS_stimuli.WE_circular05,
            "WE_circular025": RHS_stimuli.WE_circular025,
            # "grating_induction": RHS_stimuli.grating_induction,
            # "sbc_large": RHS_stimuli.sbc_large,
            # "sbc_small": RHS_stimuli.sbc_small,
            # "todorovic_equal": RHS_stimuli.todorovic_equal,
            # "todorovic_in_large": RHS_stimuli.todorovic_in_large,
            # "todorovic_in_small": RHS_stimuli.todorovic_in_small,
            # "checkerboard016": RHS_stimuli.checkerboard_016,
            # "checkerboard0938": RHS_stimuli.checkerboard_0938,
            # "checkerboard209": RHS_stimuli.checkerboard209
        }

    RHS2007 = {"models": models, "stimuli": stimuli}


def run():
    if load:
        res = load_dict("output_ODOG.pickle")
    else:
        res = main.run_model(RHS2007)
        #save_dict(res, "output_ODOG.pickle")

    res = calculate_targets_means(res)
    plot_outputs(res)
    table = create_RHS_table(res)
    html = HTML(string=table)
    #html.write_pdf("output_ODOG.pdf")

if __name__ == "__main__":
    run()
