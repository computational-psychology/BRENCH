import numpy as np
from PIL import Image

from stimuli.Stimulus import Stimulus


def adelson_checkershadow():
    image = np.array(Image.open("adelson_checkershadow.bmp").convert("L"))
    mask = np.array(Image.open("adelson_checkershadow_mask.bmp").convert("L"))

    for idx, val in enumerate(np.unique(mask)):
        mask[mask == val] = idx

    checkershadow = Stimulus()
    checkershadow.img = image
    checkershadow.target_mask = mask
    return checkershadow
