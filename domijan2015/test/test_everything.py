import os
import sys
import numpy as np
from PIL import Image

current_dir = __file__

project_path = os.path.abspath(current_dir + "../../../")
sys.path.append(project_path)
import utils, main


sep = os.path.sep
ground_truth_dir = os.path.abspath(current_dir + "../../Ground_truth") + sep

def test_everything():
    # If you only want to test certain illusions, comment out the ones you don't need
    illusions_to_test = {
        1: "dungeon_illusion",
        2: "cube_illusion",
        3: "grating_illusion",
        4: "ring_illusion",
        5: "bullseye_illusion",
        6: "SC_illusion",
        7: "white_illusion",
        8: "benarys_cross",
        9: "todorovic_illusion",
        10: "contrast_illusion",
        11: "checkerboard_illusion",
        12: "checkerboard_extended_illusion"
    }

    # same as for illusions, comment out the stuff you don't need
    parameters_to_test = (
        "c_ON",
        "c_OFF",
        "l_ON",
        "l_OFF", # not working
        "M_ON",
        "M_OFF",
        "LBD_h",
        "LBD_v",
        "GBD_h",
        "GBD_v", # not working
        "R_h",
        "R_v",
        "bright"
    )


    for i in illusions_to_test:
        img, name, _ = utils.generate_input(i)
        res = main.model(img, 20)
        for param in parameters_to_test:
            output = utils.img_to_png(res[param])
            test_output = np.asarray(
                Image.open(f"{ground_truth_dir}{name}{sep}{param}.png").convert("L")
            )
            assert utils.compare_arrays(output, test_output)
            print(f"Checked {name}, {param}")