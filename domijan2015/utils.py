import numpy as np
import io
import matplotlib.pyplot as plt
from PIL import Image




#Threshold-linear function:
def threshold(x):
    y = x * (x > 0).astype(np.float)
    return np.abs(y)


# Heaviside step function:
def heaviside(x):
    y = (x > 0).astype(np.float)
    return np.abs(y)


# Sigmoid function with S_max controlling the upper saturation point:
def sigmoid(S_max, x):
    y = (x < S_max) * (x * (x > 0).astype(np.float)) + S_max * (x >= S_max)
    return np.abs(y)


# Function that generates input image:
def generate_input(a):
    """
    Generate input image according to the passed parameter
    TODO: each call to this function should be replaced by a call to a function from the stimulus package
    """
    DUNGEON_BRESSAN_2001 = 1
    CUBE_AGOSTINI_GALMONTE_2002 = 2
    GRATING = 3
    RING_PATTERN = 4
    BULLSEYE = 5
    SIMULTANEOUS_BRIGHTNESS_CONTRAST = 6
    WHITE = 7
    BENARY_CROSS = 8
    TODOROVIC = 9
    CONTRAST_CONTRAST_EFFECT = 10
    CHECKERBOARD_CONTRAST = 11
    CHECKERBOARD_CONTRAST_EXTENDED = 12

    lum_white = 9.
    lum_black = 1.
    lum_gray = 5.

    name = ""
    if a == DUNGEON_BRESSAN_2001:
        name = "dungeon_illusion"
        cut_height = 62
        input_image = lum_black * np.ones([110, 220])
        input_image[:, 110:220] = lum_white

        for i in range(9, 90, 20):
            for j in range(9, 90, 20):
                input_image[i:i + 10, j:j + 10] = lum_white
            for j in range(119, 210, 20):
                input_image[i:i + 10, j:j + 10] = lum_black

        input_image[49:59, 29:39] = lum_gray
        input_image[49:59, 49:59] = lum_gray
        input_image[49:59, 69:79] = lum_gray
        input_image[49:59, 139:149] = lum_gray
        input_image[49:59, 159:169] = lum_gray
        input_image[49:59, 179:189] = lum_gray

        input_image[29:39, 49:59] = lum_gray
        input_image[69:79, 49:59] = lum_gray
        input_image[29:39, 159:169] = lum_gray
        input_image[69:79, 159:169] = lum_gray

    elif a == CUBE_AGOSTINI_GALMONTE_2002:
        name = "cube_illusion"
        cut_height = 48
        input_image = lum_black * np.ones([100, 200])

        input_image[:, 100:200] = lum_white
        input_image[9:20, 9:90] = lum_white
        input_image[9:90, 9:20] = lum_white
        input_image[79:90, 9:90] = lum_white
        input_image[9:90, 79:90] = lum_white

        input_image[9:20, 109:190] = lum_black
        input_image[9:90, 109:120] = lum_black
        input_image[79:90, 109:190] = lum_black
        input_image[9:90, 179:190] = lum_black

        input_image[27:32, 9:90] = lum_black
        input_image[47:52, 9:90] = lum_black
        input_image[67:72, 9:90] = lum_black

        input_image[9:90, 27:32] = lum_black
        input_image[9:90, 47:52] = lum_black
        input_image[9:90, 67:72] = lum_black

        input_image[32:47, 9:20] = lum_gray
        input_image[52:67, 79:90] = lum_gray
        input_image[79:90, 32:47] = lum_gray
        input_image[9:20, 52:67] = lum_gray

        input_image[27:32, 109:190] = lum_white
        input_image[47:52, 109:190] = lum_white
        input_image[67:72, 109:190] = lum_white

        input_image[9:90, 127:132] = lum_white
        input_image[9:90, 147:152] = lum_white
        input_image[9:90, 167:172] = lum_white

        input_image[32:47, 109:120] = lum_gray
        input_image[52:67, 179:190] = lum_gray
        input_image[79:90, 132:147] = lum_gray
        input_image[9:20, 152:167] = lum_gray

    elif a == GRATING:
        name = "grating_illusion"
        cut_height = 58
        input_image = lum_black * np.ones([100, 220])
        input_image[:, 110:220] = lum_white

        for j in range(9, 100, 20):
            input_image[9:90, j:j + 10] = lum_white

        for j in range(119, 210, 20):
            input_image[9:90, j:j + 10] = lum_black

        input_image[9:90, 49:59] = lum_gray
        input_image[9:90, 159:169] = lum_gray

    elif (a == RING_PATTERN):
        name = "ring_illusion"
        cut_height = 58
        input_image = lum_black * np.ones([100, 200])
        input_image[9:90, 9:90] = lum_white
        input_image[14:85, 14:85] = lum_black
        input_image[19:80, 19:80] = lum_white
        input_image[24:75, 24:75] = lum_gray
        input_image[29:70, 29:70] = lum_white
        input_image[34:65, 34:65] = lum_black
        input_image[39:60, 39:60] = lum_white
        input_image[44:55, 44:55] = lum_black

        input_image[9:90, 109:190] = lum_white
        input_image[14:85, 114:185] = lum_black
        input_image[19:80, 119:180] = lum_white
        input_image[24:75, 124:175] = lum_black
        input_image[29:70, 129:170] = lum_gray
        input_image[34:65, 134:165] = lum_black
        input_image[39:60, 139:160] = lum_white
        input_image[44:55, 144:155] = lum_black

    elif (a == BULLSEYE):
        name = "bullseye_illusion"
        cut_height = 58
        input_image = lum_black * np.ones([100, 200])
        input_image[9:90, 9:90] = lum_white
        input_image[14:85, 14:85] = lum_black
        input_image[19:80, 19:80] = lum_white
        input_image[24:75, 24:75] = lum_black
        input_image[29:70, 29:70] = lum_white
        input_image[34:65, 34:65] = lum_black
        input_image[39:60, 39:60] = lum_white
        input_image[44:55, 44:55] = lum_gray

        input_image[14:85, 114:185] = lum_white
        input_image[19:80, 119:180] = lum_black
        input_image[24:75, 124:175] = lum_white
        input_image[29:70, 129:170] = lum_black
        input_image[34:65, 134:165] = lum_white
        input_image[39:60, 139:160] = lum_black
        input_image[44:55, 144:155] = lum_gray

    elif (a == SIMULTANEOUS_BRIGHTNESS_CONTRAST):
        name = "SC_illusion"
        cut_height = 58
        input_image = lum_black * np.ones([100, 200])
        input_image[:, 0:100] = lum_white
        input_image[39:60, 39:60] = lum_gray
        input_image[39:60, 139:160] = lum_gray

    elif (a == WHITE):
        name = "white_illusion"
        cut_height = 58
        input_image = lum_gray * np.ones([100, 100])
        input_image[9:90, 9:19] = lum_black
        input_image[9:90, 19:29] = lum_white
        input_image[9:90, 29:39] = lum_black
        input_image[9:90, 39:49] = lum_white
        input_image[9:90, 49:59] = lum_black
        input_image[9:90, 59:69] = lum_white
        input_image[9:90, 69:79] = lum_black
        input_image[9:90, 79:89] = lum_white
        input_image[39:60, 29:39] = lum_gray
        input_image[39:60, 59:69] = lum_gray

    elif (a == BENARY_CROSS):
        name = "benarys_cross"
        cut_height = 53
        input_image = lum_white * np.ones([100, 100])
        input_image[39:60, 9:90] = lum_black
        input_image[9:90, 39:60] = lum_black
        input_image[39:50, 79:90] = lum_gray
        input_image[28:39, 28:39] = lum_gray

    elif (a == TODOROVIC):
        name = "todorovic_illusion"
        cut_height = 58
        input_image = lum_white * np.ones([100, 200])
        input_image[:, 0:100] = lum_black
        input_image[29:70, 29:70] = lum_gray
        input_image[29:70, 129:170] = lum_gray

        input_image[14:45, 14:45] = lum_white
        input_image[14:45, 54:85] = lum_white
        input_image[54:85, 14:45] = lum_white
        input_image[54:85, 54:85] = lum_white

        input_image[14:45, 114:145] = lum_black
        input_image[14:45, 154:185] = lum_black
        input_image[54:85, 114:145] = lum_black
        input_image[54:85, 154:185] = lum_black

    elif (a == CONTRAST_CONTRAST_EFFECT):
        name = "contrast_illusion"
        cut_height = 62
        input_image = lum_gray * np.ones([100, 200])
        input_image[9:89, 9:89] = lum_black

        for i in range(9, 80, 20):
            for j in range(19, 80, 20):
                input_image[i:i + 10, j:j + 10] = lum_white
                input_image[j:j + 10, i:i + 10] = lum_white

        input_image[29:69, 29:69] = (lum_white + lum_gray) / 2.
        for i in range(29, 60, 20):
            for j in range(29, 60, 20):
                input_image[i:i + 10, j:j + 10] = (lum_black + lum_gray) / 2.
                k, l = i + 10, j + 10
                input_image[k:k + 10, l:l + 10] = (lum_black + lum_gray) / 2.

        input_image[29:69, 129:169] = input_image[29:69, 29:69]

    elif (a == CHECKERBOARD_CONTRAST):
        name = "checkerboard_illusion"
        cut_height = 52
        input_image = lum_gray * np.ones([100, 100])
        input_image[9:89, 9:89] = lum_white

        for i in range(9, 80, 20):
            for j in range(9, 80, 20):
                input_image[i:i + 10, j:j + 10] = lum_black
                k, l = i + 10, j + 10
                input_image[k:k + 10, l:l + 10] = lum_black

        input_image[39:49, 29:39] = lum_gray
        input_image[59:69, 59:69] = lum_gray

    elif (a == CHECKERBOARD_CONTRAST_EXTENDED):
        name = "checkerboard_extended_illusion"
        cut_height = 52
        input_image = lum_gray * np.ones([100, 100])
        input_image[9:89, 9:89] = lum_white

        for i in range(9, 80, 20):
            for j in range(9, 80, 20):
                input_image[i:i + 10, j:j + 10] = lum_black
                k, l = i + 10, j + 10
                input_image[k:k + 10, l:l + 10] = lum_black

        input_image[39:49, 19:49] = lum_gray
        input_image[59:69, 49:79] = lum_gray
        input_image[29:59, 29:39] = lum_gray
        input_image[49:79, 59:69] = lum_gray

    else:
        raise Exception("Please provide a valid index for this function to generate input")

    return input_image, name, cut_height


def add_surround(input_raw, size=20):
    # Add mid-gray surround to the image
    M, N = input_raw.shape
    image = 5 * np.ones([M + 2 * size, N + 2 * size])
    image[size - 1:M + size - 1, size - 1:N + size - 1] = input_raw
    return image



def img_to_png(img):
    """
    Converts a numpy array to a png image in memory
    Returns a numpy array containing the data as if the image has been saved to disk and read back
    """
    try:
        tmpFile = io.BytesIO()
        plt.imsave(tmpFile, img, format="png")
        return np.asarray(Image.open(tmpFile).convert("L"))
    except Exception as e:
        print("Something went wrong trying to convert img to png. See the error below for more details.")
        raise



def compare_arrays(img1, img2, threshold=0.01):
    """
    Compares two images that are given in the form of numpy array. It computes the difference between the two arrays
    and returns true if the calculated difference divided by the number of pixels is less or equal than the given threshold (defaults to 1%)
    """
    try:
        diff = np.sum(np.abs(np.subtract(img1, img2)))
        pixels = img1.shape[0]*img1.shape[1]
        return diff/pixels < threshold
    except Exception:
        print("Something went wrong comparing arrays. See the error below for more details.")
        raise
