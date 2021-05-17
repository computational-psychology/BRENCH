import numpy as np
from scipy.signal import fftconvolve

if __package__ == None or __package__ == "":
    import utils
else:
    from . import utils


def get_contrast_pathways(xx, yy, input_image, Z):
    # Balanced center-surround RFs for contrast pathways:
    C1 = 1.  # Peak response of the center Gaussian
    S1 = 1.03361  # Peak response of the surround Gaussian
    Sigma_c = 0.5  # Width of center Gaussian
    Sigma_s = 1.5  # Width of surround Gaussian
    Gauss_con_c = C1 * np.exp(-(xx ** 2 + yy ** 2) / (2 * Sigma_c ** 2)) / (2 * np.pi * Sigma_c ** 2)
    Gauss_con_s = S1 * np.exp(-(xx ** 2 + yy ** 2) / (2 * Sigma_s ** 2)) / (2 * np.pi * Sigma_s ** 2)

    C_con = np.rot90(fftconvolve(np.rot90(input_image, 2), np.rot90(Gauss_con_c, 2), mode='same'), 2)
    S_con = np.rot90(fftconvolve(np.rot90(input_image, 2), np.rot90(Gauss_con_s, 2), mode='same'), 2)

    # Shunting / divisive inhibition; activity is defined at equilibrium
    alpha, beta, gamma = 100, 100, 100
    con_ON = (beta * C_con - gamma * S_con) / (alpha + C_con + S_con)
    con_OFF = (beta * S_con - gamma * C_con) / (alpha + C_con + S_con)

    c_ON_full  = utils.threshold(con_ON)
    c_OFF_full = utils.threshold(con_OFF)

    # Reduce output size to remove some gray background:
    M, N = input_image.shape
    c_ON = c_ON_full[Z:M - Z, Z:N - Z]
    c_OFF = c_OFF_full[Z:M - Z, Z:N - Z]

    return c_ON, c_OFF

def get_luminance_pathways(xx, yy, input_image, Z):
    # Unbalanced center-surround RFs for luminance pathways
    C2 = 1.6  # Peak response of the center Gaussian (Domijan: 1.6, Paper: 3).
    S2 = 0.5  # Peak response of the surround Gaussian (Domijan: 0.5, Paper: 1.).
    Sigma_c = 0.5  # Width of center Gaussian
    Sigma_s = 1.5  # Width of surround Gaussian
    Gauss_lum_c = C2 * np.exp(-(xx ** 2 + yy ** 2) / (2 * Sigma_c ** 2)) / (2 * np.pi * Sigma_c ** 2)
    Gauss_lum_s = S2 * np.exp(-(xx ** 2 + yy ** 2) / (2 * Sigma_s ** 2)) / (2 * np.pi * Sigma_s ** 2)

    C_lum = np.rot90(fftconvolve(np.rot90(input_image, 2), np.rot90(Gauss_lum_c, 2), mode='same'), 2)
    S_lum = np.rot90(fftconvolve(np.rot90(input_image, 2), np.rot90(Gauss_lum_s, 2), mode='same'), 2)

    # Shunting / divisive inhibition; activity is defined at equilibrium
    alpha, beta, gamma = 100, 100, 100
    lum_ON = (beta * C_lum - gamma * S_lum) / (alpha + C_lum + S_lum)
    lum_OFF = (beta * S_lum - gamma * C_lum) / (alpha + C_lum + S_lum)

    J = 10.  # the OFF Luminance activity is augmented by the tonic signal J

    l_ON_full = utils.threshold(lum_ON)
    l_OFF_full = utils.threshold(lum_OFF + J)

    # Reduce output size to remove some gray background:
    M, N = input_image.shape
    l_ON  = l_ON_full[Z:M-Z, Z:N-Z]
    l_OFF = l_OFF_full[Z:M-Z, Z:N-Z]

    return l_ON, l_OFF

# Function that generates output of the ON and OFF contrast and luminance pathways:
def run(input_image, Z):
    # RF size:
    RF_size = 15
    x = np.arange(-int(RF_size/2), int(RF_size/2)+1, 1)
    xx, yy = np.meshgrid(x, x)

    c_ON, c_OFF = get_contrast_pathways(xx, yy, input_image, Z)
    l_ON, l_OFF = get_luminance_pathways(xx, yy, input_image, Z)

    return c_ON, c_OFF, l_ON, l_OFF

