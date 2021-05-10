import numpy as np
from scipy.signal import fftconvolve
import scipy.ndimage as ndimage
import copy

if __package__ == None or __package__ == "":
    import utils
else:
    from . import utils


def get_gabor(size, k, K, Sigma_1 = 1.5, Sigma_2 = 0.5, G = 1, H = 0.5):

    """
    size: size of the filter in pixels
    k, K: used to calculate theta = 2 * PI * k/K
    Sigma_1: Width of the filter in the preferred orientation
    Sigma_2: Width of the filter in the orthogonal orientation
    G: Constant that scales the Gabor amplitude
    H: Controls the frequency of the filter's sinusoidal modulation
    """

    rec = np.floor(size / 2.)
    x = np.arange(-rec, rec + 1, 1)
    xx, yy = np.meshgrid(x, x)
    theta = (2. * np.pi * float(k)) / float(K)
    U = -xx * np.sin(theta) + yy * np.cos(theta)
    W = xx * np.cos(theta) + yy * np.sin(theta)
    Gabor = G * np.sin(H * U) * np.exp(-0.5 * ((W / Sigma_1) ** 2 + (U / Sigma_2) ** 2))
    return utils.threshold(Gabor), utils.threshold(-Gabor)


def get_simple_cells(c_ON, c_OFF, K):
    """
    c_ON/c_OFF: output off contrast pathways ON/OFF
    K: number of orientations
    """

    ON = c_ON - c_OFF
    OFF = c_OFF - c_ON

    # Parameters:
    M, N = c_ON.shape

    # Output variables for simple and complex cells with K orientations:
    simple_out = np.zeros([M, N, K])
    T_1 = 0.05  # Threshold that removes weak and noisy boundary responses (simple cell)

    # Create output of simple cortical cells:
    # For simplicity, only horizontal (k=0) and vertical (k=3) orientations
    # were used here:
    for k in range(0, K, 3):
        gaborp, gaborm = get_gabor(21, k, K)

        # The simple node is sensitive to contrast polarity thus it has two
        # lobes with opposite polarities (here: A and B)
        A_temp = np.rot90(fftconvolve(np.rot90(ON, 2), np.rot90(gaborp, 2), mode='same'), 2)
        A = utils.threshold(A_temp)
        B_temp = np.rot90(fftconvolve(np.rot90(OFF, 2), np.rot90(gaborm, 2), mode='same'), 2)
        B = utils.threshold(B_temp)

        # # Simple cell output:
        simple_out[:, :, k - 1] = utils.threshold((A + B) - np.abs(A - B) - T_1)

    return simple_out


def get_complex_cells(simple_out):
    M, N, K = simple_out.shape
    complex_out = np.zeros([M, N, K])

    ############################# Complex cells ##############################
    # Create output of complex cortical cells:
    # For this, simply add up simple cell outputs with opposite
    # contrast polarities:
    for i in range(int(K / 2)):
        complex_out[:, :, i] = simple_out[:, :, i] + simple_out[:, :, i + int(K / 2)]

    return complex_out


def LBD(complex_out, L, P):
    M, N, K = complex_out.shape
    ######################## Local boundary detection ########################
    # Prepare computation of MAX function: horizontal outputs
    LBD_h = np.zeros([M + 2 * P, N + 2 * P])
    LBD_h[P:M + P, P:N + P] = complex_out[:, :, 5]
    mask_h = utils.heaviside(LBD_h)
    temp_h = LBD_h

    # Prepare computation of MAX function: vertical outputs
    LBD_v = np.zeros([M + 2 * P, N + 2 * P])
    LBD_v[P:M + P, P:N + P] = complex_out[:, :, 2]
    mask_v = utils.heaviside(LBD_v)
    temp_v = LBD_v

    # Compute MAX function among L nearest neighbors:
    # ... for horizontal outputs:
    LBD_h_temp = LBD_h
    LBD_h_temp[L - 1:M + L + 2, 0:N + L + L + 1] = ndimage.maximum_filter(temp_h[L - 1:M + L + 2, 0:N + L + L + 1],
                                                                          size=(3, L * 2 + 1))
    LBD_h = mask_h * LBD_h_temp

    # ... for vertical outputs:
    LBD_v_temp = LBD_v
    LBD_v_temp[0:M + L + L + 1, L - 1:N + L + 2] = ndimage.maximum_filter(temp_v[0:M + L + L + 1, L - 1:N + L + 2],
                                                                          size=(L * 2 + 1, 3))
    LBD_v = mask_v * LBD_v_temp

    return LBD_h, LBD_v


def GBD(LBD_h, LBD_v, P, Q):
    M, N = LBD_h.shape
    M, N = M - 2*P, N - 2*P

    ####################### Global boundary detection ########################
    # Prepare variables for recurrent MAX function: horizontal
    temp2_h = LBD_h
    GBD_h = copy.deepcopy(LBD_h)
    mask2_h = utils.heaviside(LBD_h)
    GBD_h_temp = GBD_h

    # Prepare variables for recurrent MAX function: vertical
    temp2_v = LBD_v
    GBD_v = copy.deepcopy(LBD_v)
    mask2_v = utils.heaviside(LBD_v)
    GBD_v_temp = GBD_v

    # Recurrent computation of max function for GBD:
    GBD_steps = 20
    for t in range(GBD_steps):
        # ... for horizontal outputs
        GBD_h_temp[P - Q:M + P + Q + 1, 0:N + P + P + 1] = ndimage.maximum_filter(
            temp2_h[P - Q:M + P + Q + 1, 0:N + P + P + 1], size=(Q * 2 + 1, P * 2 + 1))
        GBD_h = mask2_h * GBD_h_temp
        temp2_h = GBD_h

        # ... for vertical outputs
        GBD_v_temp[0:M + P + P + 1, P - Q:N + P + Q + 1] = ndimage.maximum_filter(
            temp2_v[0:M + P + P + 1, P - Q:N + P + Q + 1], size=(P * 2 + 1, Q * 2 + 1))
        GBD_v = mask2_v * GBD_v_temp
        temp2_v = GBD_v

    return GBD_h, GBD_v


def LBD_GBD_interaction(LBD_h, LBD_v, GBD_h, GBD_v, T_r, F, P):
    M, N = LBD_h.shape
    M, N = M - 2 * P, N - 2 * P

    ###################### Global / local interaction ########################
    # Combine and binarize LBD and GBD outputs:
    R_h = utils.heaviside((LBD_h / (F + GBD_h)) - T_r)
    R_v = utils.heaviside((LBD_v / (F + GBD_v)) - T_r)

    # Add vertical and horizontal component:
    R_full = R_h + R_v

    # Reduce output size to remove some background:
    R = R_full[P:M + P, P:N + P]
    return R, LBD_h, LBD_v, GBD_h, GBD_v, R_h, R_v


# Function that generates output of the Boundary Contour System:
def BCS(c_ON, c_OFF):

    K = 12   # Number of orientations
    # Parameters simple cells:
    simple_out = get_simple_cells(c_ON, c_OFF, K)
    complex_out = get_complex_cells(simple_out)

    # Parameters LBD and GBD:
    L = 4    # Influences range of "horizontal connections" (Drazen: L=4, Paper: not given)
    P = 15   # Elongation of the extra-classical RF in preferred ori (Drazen: P=15, Paper: P=10)
    Q = 5    # Elongation of the extra-classical RF in orthogonal ori (Drazen: Q=5, Paper: Q=4)

    LBD_h, LBD_v = LBD(complex_out, L, P)
    GBD_h, GBD_v = GBD(LBD_h, LBD_v, P, Q)

    # Parameters LBD/GBD-interaction:
    T_r = 0.6      # Suppresses L/G Interaction output where their ratio is less than 1
    F = 0.01       # Controls the precision of the ratio computation

    return LBD_GBD_interaction(LBD_h, LBD_v, GBD_h, GBD_v, T_r, F, P)
