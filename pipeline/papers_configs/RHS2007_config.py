import stimuli
from pipeline.adapters.multyscale import main as multyscale_main
from pipeline import main, plots
import stimuli.papers.RHS2007 as RHS_stimuli

print("Initialising models...")
models = [
        {
            "name": "ODOG_BM1999",
            "runner": multyscale_main,
            "model": "ODOG_BM1999",
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
        }
    ]

print("Initialising stimuli...")
stimuli = {
        "WE_thick": RHS_stimuli.WE_thick(),
        "WE_thin_wide": RHS_stimuli.WE_thin_wide(),
        "WE_circular1": RHS_stimuli.WE_circular1(),
        "WE_circular05": RHS_stimuli.WE_circular05(),
        "WE_circular025": RHS_stimuli.WE_circular025(),
        "grating": RHS_stimuli.grating_induction(),
        "sbc_large": RHS_stimuli.sbc_large(),
        "sbc_small": RHS_stimuli.sbc_small(),
        "todorovic_equal": RHS_stimuli.todorovic_equal(),
        "todorovic_in_large": RHS_stimuli.todorovic_in_large(),
        "todorovic_in_small": RHS_stimuli.todorovic_in_small(),
        "bullseye_thin": RHS_stimuli.bullseye_thin(),
        "bullseye_thick": RHS_stimuli.bullseye_thick()
    }

RHS2007 = {"models": models, "stimuli": stimuli}

def run():
    res = main.main(RHS2007)
    plots.plot_outputs(res)

if __name__ == "__main__":
    run()
