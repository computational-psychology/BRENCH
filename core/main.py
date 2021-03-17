import sys
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# This is quite ugly, but the multyscale directory should be inside ./models in the future, so then it won't be needed anymore
current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
multyscale_path = os.path.abspath(current_dir + "../../../multyscale")
sys.path.append(multyscale_path)
import multyscale.main as ODOG


def main():
    stimuli_dir = os.path.abspath(current_dir + "/../stimuli/") + "/"

    # In these two lines the stimuli and models are specified. This is made this way just for this proof of concept and should be provided without the user having to change stuff inside this function
    stimuli_names = ["example_stimulus.png"]
    models = ["ODOG_BM1999", "LODOG_RHS2007", "FLODOG_RHS2007"]

    outputs = {}
    for model in models:
        print("Running model " + model)
        stimuli = {}
        for stim_name in stimuli_names:
            stimulus = np.asarray(Image.open(stimuli_dir + stim_name).convert("L"))
            stimuli[stim_name] = stimulus
            shape = stimulus.shape
            # Just a dummy visextent, can be easily be provided as a parameter together with stimuli_names and models
            visextent = (-16, 16, -16, 16)

        # All stimuli are provided to the model at the same time, so the model doesn't have to be recreated for each stimulus
        outputs[model] = ODOG.main(stimuli, model, shape, visextent)
        print(outputs)

    # The outputs of each model for each stimulus are returned, so the user can decide what to do with them (e.g., plot them, run calculations, save them, etc.)
    return outputs


main()
