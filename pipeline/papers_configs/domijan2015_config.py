import stimuli
from pipeline.adapters.domijan2015 import main as domijan_main
from pipeline import main, plots

print("Initialising model...")
models = [
        {
            "name": "domijan2015",
            "runner": domijan_main,
            "model": None,
            "params": {"S": 20}
        }
]
print("Initialising stimuli...")
stimuli = {
        "dungeon": stimuli.papers.domijan2015.dungeon(),
        "cube": stimuli.papers.domijan2015.cube(),
        "grating": stimuli.papers.domijan2015.grating(),
        "ring": stimuli.papers.domijan2015.rings(),
        "bullseye": stimuli.papers.domijan2015.bullseye(),
        "simultaneous brightness contrast": stimuli.papers.domijan2015.simultaneous_brightness_contrast(),
        "white": stimuli.papers.domijan2015.white(),
        "benary_cross": stimuli.papers.domijan2015.benary(),
        "todorovic": stimuli.papers.domijan2015.todorovic(),
        "checkerboard contrast-contrast": stimuli.papers.domijan2015.checkerboard_contrast_contrast(),
        "checkerboard contrast": stimuli.papers.domijan2015.checkerboard(),
        "checkerboard contrast extended": stimuli.papers.domijan2015.checkerboard_extended()
}

domijan2015 = {"models": models, "stimuli": stimuli}

def run():
    res = main.main(domijan2015)
    plots.plot_outputs(res)

if __name__ == "__main__":
    run()
