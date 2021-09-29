from pathlib import Path
import numpy as np
from PIL import Image

from stimuli.Stimulus import Stimulus

image_dir = Path(__file__).parents[0]


def adelson_checkershadow():
    image = np.array(
        Image.open(image_dir / "adelson_checkershadow.bmp").convert("L")
    )
    mask = np.array(
        Image.open(image_dir / "adelson_checkershadow_mask.bmp").convert("L")
    )

    for idx, val in enumerate(np.unique(mask)):
        mask[mask == val] = idx

    checkershadow = Stimulus()
    checkershadow.img = image
    checkershadow.target_mask = mask
    return checkershadow
