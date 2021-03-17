import sys
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

full_path = os.path.abspath(os.path.dirname(sys.argv[0]))
ODOG_path = os.path.abspath(full_path + "../../../multyscale")
sys.path.append(ODOG_path)
import multyscale.main as ODOG


def main():
    stimuli_dir = os.path.abspath(full_path + "/../stimuli/") + "/"

    stimuli_names = ["example_stimulus.png"]
    models = ["ODOG_BM1999", "LODOG_RHS2007", "FLODOG_RHS2007"]

    plt.figure()
    rows = len(models)
    cols = len(stimuli_names)
    counter = 0

    for stim_name in stimuli_names:
        for model in models:
            print("Running model " + model + " on stimulus " + stim_name)
            stimulus = np.asarray(Image.open(stimuli_dir + stim_name).convert("L"))
            shape = stimulus.shape  # filtershape in pixels
            visextent = (-16, 16, -16, 16)
            output = ODOG.main(stimulus, model, shape, visextent)
            plt.subplot(rows, cols * 2, 2 * counter + 1)
            plt.imshow(output, extent=visextent)
            plt.subplot(rows, cols * 2, 2 * counter + 2)
            plt.plot(output[512, 250:750])

            counter += 1
    plt.show()


main()
