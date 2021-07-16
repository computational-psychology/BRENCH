from weasyprint import HTML
import pickle

from pipeline.adapters.multyscale import main as multyscale_main
from pipeline import main
from pipeline.visualise_output import create_RHS_table, plot_outputs
from pipeline.postprocessing import calculate_targets_means
from pipeline.utils import save_dict, load_dict

import stimuli.papers.RHS2007 as RHS_stimuli



print("Initialising models...")
models = [
        {
            "name": "ODOG_RHS2007",
            "runner": multyscale_main,
            "model": "ODOG_RHS2007",
            "params": {"visextent": (-16,16,-16,16)}
        },
    ]

print("Initialising stimuli...")
stimuli = {
        "WE_thick": RHS_stimuli.WE_thick,
        "WE_thin_wide": RHS_stimuli.WE_thin_wide,
}

RHS2007 = {"models": models, "stimuli": stimuli}


def run():

    res = main.run_model(RHS2007)
    plot_outputs(res)
    res = calculate_targets_means(res)

    table = create_RHS_table(res)
    html = HTML(string=table)
    html.write_pdf("output_RHS_test.pdf")

if __name__ == "__main__":
    run()
