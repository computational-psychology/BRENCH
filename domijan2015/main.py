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

import numpy as np
import os

from functions import generate_input, retina, BCS, filling_in, plot1, plot2, plot3
  

# Run the simulations for 12 brightness illusions:
for i in range(12):
    
    print('Model simulations for stimulus: ' + str(i+1))
    
    ###################################
    #            Parameters           #
    ###################################
    # Select one brightness illusion:
    chosen_input = i+1
    
    # Do you want to save the result plots?
    save_plot = True
    

    ###################################
    #              Main               #
    ###################################
    # Create input image
    input_raw = generate_input(chosen_input)
    
    # Add mid-gray surround to the image
    S = 20
    M, N = input_raw.shape
    input_image = 5 * np.ones([M+2*S, N+2*S])
    input_image[S-1:M+S-1, S-1:N+S-1] = input_raw
    
    # Extract contrast and luminance information:
    c_ON, c_OFF, l_ON, l_OFF = retina(input_image, int(S/2))
    
    # Contrast and luminance integration in the ON channel:
    w1 = 3.
    w2 = 1.
    m_ON  = w1*c_ON  + w2*l_ON
    
    # Contrast and lumiance integration in the OFF channel
    m_OFF = w1*c_OFF + w2*l_OFF
    
    # Contour detection and processing:
    R, LBD_h, LBD_v, GBD_h, GBD_v, R_h, R_v = BCS(c_ON, c_OFF)
    
    # Filling-in:
    bright, M_ON, M_OFF, _, _ = filling_in(R, m_ON, m_OFF)
    
    
    ###################################
    #            Figures              #
    ###################################
    # Some preparations for plotting and saving the model outputs:
    if chosen_input==1:
        illusion_name = 'dungeon_illusion'
        cut_height = 62
    if chosen_input==2:
        illusion_name = 'cube_illusion'
        cut_height = 48
    if chosen_input==3:
        illusion_name = 'grating_illusion'
        cut_height = 58
    if chosen_input==4:
        illusion_name = 'ring_illusion'
        cut_height = 58
    if chosen_input==5:
        illusion_name = 'bullseye_illusion'
        cut_height = 58
    if chosen_input==6:
        illusion_name = 'SC_illusion'
        cut_height = 58
    if chosen_input==7:
        illusion_name = 'white_illusion'
        cut_height = 58
    if chosen_input==8:
        illusion_name = 'benarys_cross'
        cut_height = 53
    if chosen_input==9:
        illusion_name = 'todorovic_illusion'
        cut_height = 58
    if chosen_input==10:
        illusion_name = 'contrast_illusion'
        cut_height = 62
    if chosen_input==11:
        illusion_name = 'checkerboard_illusion'
        cut_height = 52
    if chosen_input==12:
        illusion_name = 'checkerboard_extended_illusion'
        cut_height = 52
    if chosen_input>12:
        # It is possible to add more stimuli to the generate_input function.
        # If so, their model outputs will be called '_test'
        illusion_name = '_test'
        cut_height = 58
    
    
    if save_plot:
        # Create outputs folder:
        result_folder = 'outputs/'
        save_path = result_folder + illusion_name
        if not os.path.exists(result_folder):
            os.mkdir(result_folder)
        
        # Plot 1: Contrast, luminance and filling-in outputs
        plot1(save_path, c_ON, c_OFF, l_ON, l_OFF, M_ON, M_OFF)
        
        # Plot 2: BCS outputs
        plot2(save_path, LBD_h, LBD_v, GBD_h, GBD_v, R_h, R_v)
        
        # Plot 3: Brightness estimate
        plot3(save_path, input_image, bright, cut_height, N+S)
        
    print('...')

