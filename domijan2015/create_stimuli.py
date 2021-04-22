import functions
import numpy as np
from PIL import Image

for a in range(1, 12):
    data = functions.generate_input(a)
    rescaled = (255.0 / data.max() * (data - data.min())).astype(np.uint8)
    im = Image.fromarray(rescaled)
    im.save("stimuli/" + str(a) + ".png")
