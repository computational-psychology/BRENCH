"""
This Python code was adapted from MATLAB scripts that were kindly provided by
Drazan Domijan.

It contains additional functions relevant for the brightess perception model
described in:
Domijan (2015): A Neurocomputational account of the role of contour facilitation
in brightness perception

@author: lynn schmittwilken
"""

import numpy as np
import copy
from scipy.signal import fftconvolve
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


###################################
#            Functions            #
###################################
# Threshold-linear function:
def f_fun(x):
    y = x * (x > 0).astype(np.float)
    return np.abs(y)


# Heaviside step function:
def h_fun(x):
    y = (x > 0).astype(np.float)
    return np.abs(y)


# Sigmoid function with S_max controlling the upper saturation point:
def s_fun(S_max, x):
    y = (x < S_max) * (x * (x > 0).astype(np.float)) + S_max * (x >= S_max)
    return np.abs(y)


# Function that generates input image:
def generate_input(a):
    lum_white = 9.0
    lum_black = 1.0
    lum_gray = 5.0

    # TODO: put these model constants in some sort of Enum to avoid using magic numbers
    # TODO: Put all input creation functions in a separate file

    if a == 1:
        # Dungeon illusion (Bressan, 2001)
        input_image = lum_black * np.ones([110, 220])
        input_image[:, 110:220] = lum_white

        for i in range(9, 90, 20):
            for j in range(9, 90, 20):
                input_image[i : i + 10, j : j + 10] = lum_white
            for j in range(119, 210, 20):
                input_image[i : i + 10, j : j + 10] = lum_black

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

    if a == 2:
        # Cube illusion (Agostini & Galmonte, 2002)
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

    if a == 3:
        # Grating illusion
        input_image = lum_black * np.ones([100, 220])
        input_image[:, 110:220] = lum_white

        for j in range(9, 100, 20):
            input_image[9:90, j : j + 10] = lum_white

        for j in range(119, 210, 20):
            input_image[9:90, j : j + 10] = lum_black

        input_image[9:90, 49:59] = lum_gray
        input_image[9:90, 159:169] = lum_gray

    if a == 4:
        # Ring pattern
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

    if a == 5:
        # Bullseye illusion
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

    if a == 6:
        # Simultaneous brightness contrast
        input_image = lum_black * np.ones([100, 200])
        input_image[:, 0:100] = lum_white
        input_image[39:60, 39:60] = lum_gray
        input_image[39:60, 139:160] = lum_gray

    if a == 7:
        # White illusion
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

    if a == 8:
        # Benary's cross
        input_image = lum_white * np.ones([100, 100])
        input_image[39:60, 9:90] = lum_black
        input_image[9:90, 39:60] = lum_black
        input_image[39:50, 79:90] = lum_gray
        input_image[28:39, 28:39] = lum_gray

    if a == 9:
        # Todorovic's illusion
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

    if a == 10:
        # Contrast-contrast effect
        input_image = lum_gray * np.ones([100, 200])
        input_image[9:89, 9:89] = lum_black

        for i in range(9, 80, 20):
            for j in range(19, 80, 20):
                input_image[i : i + 10, j : j + 10] = lum_white
                input_image[j : j + 10, i : i + 10] = lum_white

        input_image[29:69, 29:69] = (lum_white + lum_gray) / 2.0
        for i in range(29, 60, 20):
            for j in range(29, 60, 20):
                input_image[i : i + 10, j : j + 10] = (lum_black + lum_gray) / 2.0
                k, l = i + 10, j + 10
                input_image[k : k + 10, l : l + 10] = (lum_black + lum_gray) / 2.0

        input_image[29:69, 129:169] = input_image[29:69, 29:69]

    if a == 11:
        # Checkerboard contrast
        input_image = lum_gray * np.ones([100, 100])
        input_image[9:89, 9:89] = lum_white

        for i in range(9, 80, 20):
            for j in range(9, 80, 20):
                input_image[i : i + 10, j : j + 10] = lum_black
                k, l = i + 10, j + 10
                input_image[k : k + 10, l : l + 10] = lum_black

        input_image[39:49, 29:39] = lum_gray
        input_image[59:69, 59:69] = lum_gray

    if a == 12:
        # Extended version of checkerboard contrast
        input_image = lum_gray * np.ones([100, 100])
        input_image[9:89, 9:89] = lum_white

        for i in range(9, 80, 20):
            for j in range(9, 80, 20):
                input_image[i : i + 10, j : j + 10] = lum_black
                k, l = i + 10, j + 10
                input_image[k : k + 10, l : l + 10] = lum_black

        input_image[39:49, 19:49] = lum_gray
        input_image[59:69, 49:79] = lum_gray
        input_image[29:59, 29:39] = lum_gray
        input_image[49:79, 59:69] = lum_gray

    return input_image


# Function that generates output of the ON and OFF contrast and luminance pathways:
def retina(input_image, Z):
    # RF size:
    RF_size = 15
    x = np.arange(-int(RF_size / 2), int(RF_size / 2) + 1, 1)
    xx, yy = np.meshgrid(x, x)

    # Balanced center-surround RFs for contrast pathways:
    C1 = 1.0  # Peak response of the center Gaussian
    S1 = 1.03361  # Peak response of the surround Gaussian
    Sigma_c = 0.5  # Width of center Gaussian
    Sigma_s = 1.5  # Width of surround Gaussian
    Gauss_con_c = (
        C1
        * np.exp(-(xx ** 2 + yy ** 2) / (2 * Sigma_c ** 2))
        / (2 * np.pi * Sigma_c ** 2)
    )
    Gauss_con_s = (
        S1
        * np.exp(-(xx ** 2 + yy ** 2) / (2 * Sigma_s ** 2))
        / (2 * np.pi * Sigma_s ** 2)
    )

    # Unbalanced center-surround RFs for luminance pathways
    C2 = 1.6  # Peak response of the center Gaussian (Domijan: 1.6, Paper: 3).
    S2 = 0.5  # Peak response of the surround Gaussian (Domijan: 0.5, Paper: 1.).
    Gauss_lum_c = (
        C2
        * np.exp(-(xx ** 2 + yy ** 2) / (2 * Sigma_c ** 2))
        / (2 * np.pi * Sigma_c ** 2)
    )
    Gauss_lum_s = (
        S2
        * np.exp(-(xx ** 2 + yy ** 2) / (2 * Sigma_s ** 2))
        / (2 * np.pi * Sigma_s ** 2)
    )

    # Convolving input with RFs:
    C_con = np.rot90(
        fftconvolve(np.rot90(input_image, 2), np.rot90(Gauss_con_c, 2), mode="same"), 2
    )
    S_con = np.rot90(
        fftconvolve(np.rot90(input_image, 2), np.rot90(Gauss_con_s, 2), mode="same"), 2
    )
    C_lum = np.rot90(
        fftconvolve(np.rot90(input_image, 2), np.rot90(Gauss_lum_c, 2), mode="same"), 2
    )
    S_lum = np.rot90(
        fftconvolve(np.rot90(input_image, 2), np.rot90(Gauss_lum_s, 2), mode="same"), 2
    )

    # Shunting / divisive inhibition; activity is defined at equilibrium
    alpha = 100.0
    beta = 100.0
    gamma = 100.0
    con_ON = (beta * C_con - gamma * S_con) / (alpha + C_con + S_con)
    con_OFF = (beta * S_con - gamma * C_con) / (alpha + C_con + S_con)
    lum_ON = (beta * C_lum - gamma * S_lum) / (alpha + C_lum + S_lum)
    lum_OFF = (beta * S_lum - gamma * C_lum) / (alpha + C_lum + S_lum)

    # # Eliminate negative values:
    J = 10.0  # the OFF Luminance activity is augmented by the tonic signal J
    c_ON_full = f_fun(con_ON)
    c_OFF_full = f_fun(con_OFF)
    l_ON_full = f_fun(lum_ON)
    l_OFF_full = f_fun(lum_OFF + J)

    # Reduce output size to remove some gray background:
    M, N = input_image.shape
    c_ON = c_ON_full[Z : M - Z, Z : N - Z]
    c_OFF = c_OFF_full[Z : M - Z, Z : N - Z]
    l_ON = l_ON_full[Z : M - Z, Z : N - Z]
    l_OFF = l_OFF_full[Z : M - Z, Z : N - Z]
    return c_ON, c_OFF, l_ON, l_OFF


# Function that generates output of the Boundary Contour System:
def BCS(c_ON, c_OFF):
    # Inputs:
    ON = c_ON - c_OFF
    OFF = c_OFF - c_ON

    # Parameters:
    M, N = c_ON.shape

    # Parameters simple cells:
    K = 12  # Total number of orientations
    Sigma_1 = 1.5  # Width of the filter in the preferred orientation
    Sigma_2 = 0.5  # Width of the filter in the orthogonal orientation
    G = 1.0  # Constant that scales the Gabor amplitude
    H = 0.5  # Controls the frequency of the filter's sinusoidal modulation
    T_1 = 0.05  # Threshold that removes weak and noisy boundary responses (simple cell)

    # Parameters LBD and GBD:
    L = (
        4
    )  # Influences range of "horizontal connections" (Drazen: L=4, Paper: not given)
    P = (
        15
    )  # Elongation of the extra-classical RF in preferred ori (Drazen: P=15, Paper: P=10)
    Q = (
        5
    )  # Elongation of the extra-classical RF in orthogonal ori (Drazen: Q=5, Paper: Q=4)

    # Parameters LBD/GBD-interaction:
    T_r = 0.6  # Suppresses L/G Interaction output where their ratio is less than 1
    F = 0.01  # Controls the precision of the ratio computation

    # Prepare Gabor:
    gabor_size = 21
    rec = np.floor(gabor_size / 2.0)
    x = np.arange(-rec, rec + 1, 1)
    xx, yy = np.meshgrid(x, x)

    # Output variables for simple and complex cells with K orientations:
    simple_out = np.zeros([M, N, K])
    complex_out = np.zeros([M, N, K])

    ############################# Simple cells ###############################
    # Create output of simple cortical cells:
    # For simplicity, only horizontal (k=3) and vertical (k=6) orientations
    # were used here:
    for k in range(3, K + 1, 3):
        # Orientation:
        theta = (2.0 * np.pi * float(k)) / float(K)
        U = -xx * np.sin(theta) + yy * np.cos(theta)
        W = xx * np.cos(theta) + yy * np.sin(theta)

        # Create Gabors:
        Gabor = (
            G * np.sin(H * U) * np.exp(-0.5 * ((W / Sigma_1) ** 2 + (U / Sigma_2) ** 2))
        )
        Gaborp = f_fun(Gabor)
        Gaborm = f_fun(-Gabor)

        # The simple node is sensitive to contrast polarity thus it has two
        # lobes with opposite polarities (here: A and B)
        A_temp = np.rot90(
            fftconvolve(np.rot90(ON, 2), np.rot90(Gaborp, 2), mode="same"), 2
        )
        A = f_fun(A_temp)
        B_temp = np.rot90(
            fftconvolve(np.rot90(OFF, 2), np.rot90(Gaborm, 2), mode="same"), 2
        )
        B = f_fun(B_temp)

        # # Simple cell output:
        simple_out[:, :, k - 1] = f_fun((A + B) - np.abs(A - B) - T_1)

    ############################# Complex cells ##############################
    # Create output of complex cortical cells:
    # For this, simply add up simple cell outputs with opposite
    # contrast polarities:
    for i in range(int(K / 2)):
        complex_out[:, :, i] = simple_out[:, :, i] + simple_out[:, :, i + int(K / 2)]

    ######################## Local boundary detection ########################
    # Prepare computation of MAX function: horizontal outputs
    LBD_h = np.zeros([M + 2 * P, N + 2 * P])
    LBD_h[P : M + P, P : N + P] = complex_out[:, :, 5]
    mask_h = h_fun(LBD_h)
    temp_h = LBD_h

    # Prepare computation of MAX function: vertical outputs
    LBD_v = np.zeros([M + 2 * P, N + 2 * P])
    LBD_v[P : M + P, P : N + P] = complex_out[:, :, 2]
    mask_v = h_fun(LBD_v)
    temp_v = LBD_v

    # Compute MAX function among L nearest neighbors:
    # ... for horizontal outputs:
    LBD_h_temp = LBD_h
    LBD_h_temp[L - 1 : M + L + 2, 0 : N + L + L + 1] = ndimage.maximum_filter(
        temp_h[L - 1 : M + L + 2, 0 : N + L + L + 1], size=(3, L * 2 + 1)
    )
    LBD_h = mask_h * LBD_h_temp

    # ... for vertical outputs:
    LBD_v_temp = LBD_v
    LBD_v_temp[0 : M + L + L + 1, L - 1 : N + L + 2] = ndimage.maximum_filter(
        temp_v[0 : M + L + L + 1, L - 1 : N + L + 2], size=(L * 2 + 1, 3)
    )
    LBD_v = mask_v * LBD_v_temp

    ####################### Global boundary detection ########################
    # Prepare variables for recurrent MAX function: horizontal
    temp2_h = LBD_h
    GBD_h = copy.deepcopy(LBD_h)
    mask2_h = h_fun(LBD_h)
    GBD_h_temp = GBD_h

    # Prepare variables for recurrent MAX function: vertical
    temp2_v = LBD_v
    GBD_v = copy.deepcopy(LBD_v)
    mask2_v = h_fun(LBD_v)
    GBD_v_temp = GBD_v

    # Recurrent computation of max function for GBD:
    GBD_steps = 20
    for t in range(GBD_steps):
        # ... for horizontal outputs
        GBD_h_temp[P - Q : M + P + Q + 1, 0 : N + P + P + 1] = ndimage.maximum_filter(
            temp2_h[P - Q : M + P + Q + 1, 0 : N + P + P + 1],
            size=(Q * 2 + 1, P * 2 + 1),
        )
        GBD_h = mask2_h * GBD_h_temp
        temp2_h = GBD_h

        # ... for vertical outputs
        GBD_v_temp[0 : M + P + P + 1, P - Q : N + P + Q + 1] = ndimage.maximum_filter(
            temp2_v[0 : M + P + P + 1, P - Q : N + P + Q + 1],
            size=(P * 2 + 1, Q * 2 + 1),
        )
        GBD_v = mask2_v * GBD_v_temp
        temp2_v = GBD_v

    ###################### Global / local interaction ########################
    # Combine and binarize LBD and GBD outputs:
    R_h = h_fun((LBD_h / (F + GBD_h)) - T_r)
    R_v = h_fun((LBD_v / (F + GBD_v)) - T_r)

    # Add vertical and horizontal component:
    R_full = R_h + R_v

    # Reduce output size to remove some background:
    R = R_full[P : M + P, P : N + P]
    return R, LBD_h, LBD_v, GBD_h, GBD_v, R_h, R_v


# Function that generates brightness percept based on filing-in:
def filling_in(R, m_ON, m_OFF):
    M, N = m_ON.shape
    epsilon = 10.0  # Controls the strength of divisive inhibition
    T_f = 3.0  # Prevents filling-in for weak luminance and contrast signals

    # Initiate all relevant variables:
    # NOTE: We initiate all variable slightly larger than
    # before in order to efficiently compute the MAX function

    # Edge map from BCS that prevents acitivity spreading across edges:
    edge = np.zeros([M + 2, N + 2])
    edge[1 : M + 1, 1 : N + 1] = R

    # Threshold outputs from the ON and OFF Contrast and Luminance Pathways
    # for filling-in:
    M_ON = np.zeros([M + 2, N + 2])
    M_ON[1 : M + 1, 1 : N + 1] = s_fun(14.0, m_ON)
    M_ON_temp = copy.deepcopy(M_ON)

    M_OFF = np.zeros([M + 2, N + 2])
    M_OFF[1 : M + 1, 1 : N + 1] = s_fun(14.0, m_OFF)
    M_OFF_temp = copy.deepcopy(M_OFF)

    # Binarize outputs from the ON and OFF Contrast and Luminance Pathways
    # in order to prevent spreading to non-active units:
    mask_ON = np.zeros([M + 2, N + 2])
    mask_ON[1 : M + 1, 1 : N + 1] = h_fun(m_ON - T_f)

    mask_OFF = np.zeros([M + 2, N + 2])
    mask_OFF[1 : M + 1, 1 : N + 1] = h_fun(m_OFF - T_f)

    # Some variables to efficiently compute the MAX function between
    # neighboring pixels:
    top_ON = np.zeros([M + 2, N + 2])
    bottom_ON = np.zeros([M + 2, N + 2])
    left_ON = np.zeros([M + 2, N + 2])
    right_ON = np.zeros([M + 2, N + 2])

    top_OFF = np.zeros([M + 2, N + 2])
    bottom_OFF = np.zeros([M + 2, N + 2])
    left_OFF = np.zeros([M + 2, N + 2])
    right_OFF = np.zeros([M + 2, N + 2])

    # In order to visualize the filling-in process over time:
    fill_steps = 300  # (Domijan: 300, Paper: 200)
    M_ON_vid = np.zeros([M + 2, N + 2, fill_steps])
    M_OFF_vid = np.zeros([M + 2, N + 2, fill_steps])

    # Compute the recurrent MAX function among the nearest neighbors
    # (one pixel up, down, left, right)
    for t in range(fill_steps):
        # Select the nearest neighbors (top, bottom, left, right)
        # IMPORTANT: Activity at borders is "penalized" / strongly reduced
        top_ON[1 : M + 1, 1 : N + 1] = M_ON[0:M, 1 : N + 1] / (
            1 + epsilon * edge[0:M, 1 : N + 1] * edge[1 : M + 1, 1 : N + 1]
        )
        bottom_ON[1 : M + 1, 1 : N + 1] = M_ON[2 : M + 2, 1 : N + 1] / (
            1 + epsilon * edge[2 : M + 2, 1 : N + 1] * edge[1 : M + 1, 1 : N + 1]
        )
        left_ON[1 : M + 1, 1 : N + 1] = M_ON[1 : M + 1, 0:N] / (
            1 + epsilon * edge[1 : M + 1, 0:N] * edge[1 : M + 1, 1 : N + 1]
        )
        right_ON[1 : M + 1, 1 : N + 1] = M_ON[1 : M + 1, 2 : N + 2] / (
            1 + epsilon * edge[1 : M + 1, 2 : N + 2] * edge[1 : M + 1, 1 : N + 1]
        )

        # Select the nearest neighbors (top, bottom, left, right)
        # IMPORTANT: Activity at borders is "penalized" / strongly reduced
        top_OFF[1 : M + 1, 1 : N + 1] = M_OFF[0:M, 1 : N + 1] / (
            1 + epsilon * edge[0:M, 1 : N + 1] * edge[1 : M + 1, 1 : N + 1]
        )
        bottom_OFF[1 : M + 1, 1 : N + 1] = M_OFF[2 : M + 2, 1 : N + 1] / (
            1 + epsilon * edge[2 : M + 2, 1 : N + 1] * edge[1 : M + 1, 1 : N + 1]
        )
        left_OFF[1 : M + 1, 1 : N + 1] = M_OFF[1 : M + 1, 0:N] / (
            1 + epsilon * edge[1 : M + 1, 0:N] * edge[1 : M + 1, 1 : N + 1]
        )
        right_OFF[1 : M + 1, 1 : N + 1] = M_OFF[1 : M + 1, 2 : N + 2] / (
            1 + epsilon * edge[1 : M + 1, 2 : N + 2] * edge[1 : M + 1, 1 : N + 1]
        )

        # Select the MAX value between top_ON, bottom_ON, left_ON, right_ON:
        M_ON_temp[1 : M + 1, 1 : N + 1] = np.maximum(
            top_ON[1 : M + 1, 1 : N + 1], bottom_ON[1 : M + 1, 1 : N + 1]
        )
        M_ON_temp[1 : M + 1, 1 : N + 1] = np.maximum(
            M_ON_temp[1 : M + 1, 1 : N + 1], left_ON[1 : M + 1, 1 : N + 1]
        )
        M_ON_temp[1 : M + 1, 1 : N + 1] = np.maximum(
            M_ON_temp[1 : M + 1, 1 : N + 1], right_ON[1 : M + 1, 1 : N + 1]
        )

        # Select the MAX value between top_OFF, bottom_OFF, left_OFF, right_OFF:
        M_OFF_temp[1 : M + 1, 1 : N + 1] = np.maximum(
            top_OFF[1 : M + 1, 1 : N + 1], bottom_OFF[1 : M + 1, 1 : N + 1]
        )
        M_OFF_temp[1 : M + 1, 1 : N + 1] = np.maximum(
            M_OFF_temp[1 : M + 1, 1 : N + 1], left_OFF[1 : M + 1, 1 : N + 1]
        )
        M_OFF_temp[1 : M + 1, 1 : N + 1] = np.maximum(
            M_OFF_temp[1 : M + 1, 1 : N + 1], right_OFF[1 : M + 1, 1 : N + 1]
        )

        M_ON = np.maximum(M_ON, (mask_ON * M_ON_temp))
        M_OFF = np.maximum(M_OFF, (mask_OFF * M_OFF_temp))

        M_ON_vid[:, :, t] = M_ON
        M_OFF_vid[:, :, t] = M_OFF

    bright_raw = f_fun(M_ON[1 : M + 1, 1 : N + 1] - T_f) - f_fun(
        M_OFF[1 : M + 1, 1 : N + 1] - T_f
    )
    bright_raw = bright_raw + np.abs(bright_raw.min())
    bright = bright_raw / bright_raw.max()
    return bright, M_ON, M_OFF, M_ON_vid, M_OFF_vid


# Plot first part of results:
def plot1(save_path, c_ON, c_OFF, l_ON, l_OFF, M_ON, M_OFF):
    cmap = "coolwarm"
    plt.figure(figsize=(15, 15))
    plt.subplot(321)
    plt.imshow(c_ON, cmap=cmap)
    plt.axis("off")
    plt.title("ON network: contrast")
    plt.clim(-c_ON.max(), c_ON.max())
    plt.colorbar()

    plt.subplot(322)
    plt.imshow(c_OFF, cmap=cmap)
    plt.axis("off")
    plt.title("OFF network: contrast")
    plt.clim(-c_OFF.max(), c_OFF.max())
    plt.colorbar()

    plt.subplot(323)
    plt.imshow(l_ON, cmap=cmap)
    plt.axis("off")
    plt.title("ON network: luminance")
    plt.clim(-l_ON.max(), l_ON.max())
    plt.colorbar()

    plt.subplot(324)
    plt.imshow(l_OFF, cmap=cmap)
    plt.axis("off")
    plt.title("OFF network: luminance")
    plt.clim(-l_OFF.max(), l_OFF.max())
    plt.colorbar()

    plt.subplot(325)
    plt.imshow(M_ON, cmap=cmap)
    plt.axis("off")
    plt.title("ON network: filled")
    plt.clim(-M_ON.max(), M_ON.max())
    plt.colorbar()

    plt.subplot(326)
    plt.imshow(M_OFF, cmap=cmap)
    plt.axis("off")
    plt.title("OFF network: filled")
    plt.clim(-M_OFF.max(), M_OFF.max())
    plt.colorbar()
    plt.savefig(save_path + "1.png")
    plt.close()


# Plot second part of results:
def plot2(save_path, LBD_h, LBD_v, GBD_h, GBD_v, R_h, R_v):
    cmap = "coolwarm"
    plt.figure(figsize=(15, 15))
    plt.subplot(321)
    plt.imshow(LBD_h, cmap=cmap)
    plt.axis("off")
    plt.title("Local boundaries")
    plt.clim(-LBD_h.max(), LBD_h.max())
    plt.colorbar()

    plt.subplot(322)
    plt.imshow(LBD_v, cmap=cmap)
    plt.axis("off")
    plt.title("Local boundaries")
    plt.clim(-LBD_v.max(), LBD_v.max())
    plt.colorbar()

    plt.subplot(323)
    plt.imshow(GBD_h, cmap=cmap)
    plt.axis("off")
    plt.title("Global boundaries")
    plt.clim(-GBD_h.max(), GBD_h.max())
    plt.colorbar()

    plt.subplot(324)
    plt.imshow(GBD_v, cmap=cmap)
    plt.axis("off")
    plt.title("Global boundaries")
    plt.clim(-GBD_v.max(), GBD_v.max())
    plt.colorbar()

    plt.subplot(325)
    plt.imshow(R_h, cmap=cmap)
    plt.axis("off")
    plt.title("Integration")
    plt.clim(-R_h.max(), R_h.max())
    plt.colorbar()

    plt.subplot(326)
    plt.imshow(R_v, cmap=cmap)
    plt.axis("off")
    plt.title("Integration")
    plt.clim(-R_v.max(), R_v.max())
    plt.colorbar()
    plt.savefig(save_path + "2.png")
    plt.close()


# Plot third part of results:
def plot3(save_path, input_image, bright, cut_height, NS):
    plt.figure(figsize=(22, 6))
    plt.subplot(131)
    plt.imshow(input_image, cmap="gray")
    plt.title("Input stimulus")
    plt.colorbar()

    plt.subplot(132)
    plt.imshow(bright, cmap="coolwarm")
    plt.axhline(y=cut_height, color="k")
    plt.title("Brightness output")
    plt.clim(-bright.max(), bright.max())
    plt.colorbar()

    plt.subplot(133)
    x_ax = np.arange(0, np.size(bright, 1))
    plt.plot(x_ax, np.squeeze(bright[cut_height, :]), "k")
    plt.ylim([-0.1, 1.1])
    plt.xlim([0, NS])
    plt.title("Cut through")
    plt.savefig(save_path + "3.png")
    plt.close()


# Save a video:
def save_video(video1, video2, fname, fps, figsize=(10, 3)):
    """
    Save 3D arrays as MP4 videos, using matplotlib.animate.
    parameters
    ------------
    video - 3D array, where the last dimension is the time dimension
    fname - file basename (without type ending)
    figsize - of underlying matplotlib figure
    """
    fig = plt.figure(figsize=figsize)
    ax1 = plt.subplot(121)
    im1 = plt.imshow(
        video1[:, :, 0], cmap="coolwarm", vmin=video1.min(), vmax=video1.max()
    )
    plt.clim(-video1.max(), video1.max())
    plt.title("ON pathway: Frame 000")
    plt.axis("off")
    ax2 = plt.subplot(122)
    im2 = plt.imshow(
        video2[:, :, 0], cmap="coolwarm", vmin=video2.min(), vmax=video2.max()
    )
    plt.clim(-video2.max(), video2.max())
    plt.title("OFF pathway: Frame 000")
    plt.axis("off")

    def animate(i):
        im1.set_array(video1[:, :, i])
        ax1.set_title(f"ON pathway: Frame {i:03d}")
        plt.axis("off")

        im2.set_array(video2[:, :, i])
        ax2.set_title(f"OFF pathway: Frame {i:03d}")
        plt.axis("off")

    n_frames = np.size(video1, 2)
    anim = FuncAnimation(fig, animate, frames=n_frames)
    anim.save("%s.gif" % fname, writer="imagemagick", fps=10)
    plt.close()
