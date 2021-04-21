import sys
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# This is quite ugly, but the multyscale directory should be inside ./models in the future, so then it won't be needed anymore
current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
multyscale_path = os.path.abspath(current_dir + "../../../multyscale/")
sys.path.append(multyscale_path)
from multyscale import main as ODOG


def main():
    stimuli_dir = os.path.abspath(current_dir + "/../stimuli/") + "/"

    # In these two lines the stimuli and models are specified. This is made this way just for this proof of concept and should be provided without the user having to change stuff inside this function
    #stimuli_names = ["1.png", "2.png", "example_stimulus.png"]
    stimuli_names = ["example_stimulus.png"]
    models = ["ODOG_BM1999", "LODOG_RHS2007", "FLODOG_RHS2007"]

    outputs = {}
    for model in models:
        # print("Running model " + model)
        stimuli = {}
        for stim_name in stimuli_names:
            stimulus = np.asarray(Image.open(stimuli_dir + stim_name).convert("L"))
            # PIL has height as first shape element and width as second which is not analogous with the usual (x,y) approach, therefore the two axes are swapped.
            stimuli[stim_name] = stimulus
            # Just a dummy visextent, can be easily be provided as a parameter together with stimuli_names and models

        visextent = (-16, 16, -16, 16)
        outputs[model] = ODOG.main(stimuli, model, visextent)

    # The outputs of each model for each stimulus are returned, so the user can decide what to do with them (e.g., plot them, run calculations, save them, etc.)
    return outputs


res = main()

fig = plt.figure(figsize=[10, 20])
counter = 1
for model_name, model_output in res.items():
    print(model_name)
    for stimulus, output in model_output.items():
        plt.subplot(3, 1, counter)
        counter += 1
        plt.title(model_name + " - " + stimulus)
        plt.imshow(output)
plt.show()
