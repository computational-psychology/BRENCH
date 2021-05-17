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

if __package__ == None or __package__ == "":
    import utils, retina, boundary_detection, filling_in
else:
    from . import utils, retina, boundary_detection, filling_in


# Run the simulations for 12 brightness illusions:
def main(model_class, params, stimuli):
    # Model class is not used

    S = params["S"]
    outputs = {}
    for stimulus_name, stimulus in stimuli.items():
        input_image = utils.add_surround(stimulus, S)

        # Extract contrast and luminance information:
        c_ON, c_OFF, l_ON, l_OFF = retina.run(input_image, int(S / 2))

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

        outputs[stimulus_name] = {"c_ON": c_ON, "c_OFF": c_OFF, "l_ON": l_ON, "l_OFF": l_OFF, "M_ON": M_ON, "M_OFF": M_OFF, "LBD_h": LBD_h,
                "LBD_v": LBD_v, "GBD_h":GBD_h, "GBD_v": GBD_v, "R_h": R_h, "R_v": R_v, "bright": bright, "image": bright}

    return outputs

