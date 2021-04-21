"""
This Python code was adapted from MATLAB scripts that were kindly provided by
Drazan Domijan.

This code contains the re-implementation of the brightness perception model
described in:
Domijan (2015): A Neurocomputational account of the role of contour facilitation
in brightness perception

It can be used to reproduce all the results that were presented in the paper.
For more details, see functions.py

@author: lynn schmittwilken
"""

import utils
import retina
import boundary_detection
import filling_in

# Run the simulations for 12 brightness illusions:
def model(input_raw, S):
    input_image = utils.add_surround(input_raw, S)
    
    # Extract contrast and luminance information:
    c_ON, c_OFF, l_ON, l_OFF = retina.run(input_image, int(S/2))
    
    # Contrast and luminance integration in the ON channel:
    w1 = 3.
    w2 = 1.
    m_ON  = w1*c_ON  + w2*l_ON
    
    # Contrast and lumiance integration in the OFF channel
    m_OFF = w1*c_OFF + w2*l_OFF
    
    # Contour detection and processing:
    R, LBD_h, LBD_v, GBD_h, GBD_v, R_h, R_v = boundary_detection.BCS(c_ON, c_OFF)
    
    # Filling-in:
    bright, M_ON, M_OFF, _, _ = filling_in.fill_in(R, m_ON, m_OFF)
    
    return {"c_ON": c_ON, "c_OFF": c_OFF, "l_ON": l_ON, "l_OFF": l_OFF, "M_ON": M_ON, "M_OFF": M_OFF, "LBD_h": LBD_h,
            "LBD_v": LBD_v, "GBD_h":GBD_h, "GBD_v": GBD_v, "R_h": R_h, "R_v": R_v, "bright": bright}

