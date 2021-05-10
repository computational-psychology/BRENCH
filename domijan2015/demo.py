import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import utils
import main

# Do you want to save the result plots?
def run_demo():
    save_plot = True
    cut_height = 55
    S = 20
    for i in range(1, 13): # if you want to run only specific inputs, use list of the indices you want instead of range(1,13)
        print("doing ", str(i))
        input, illusion_name, cut_height = utils.generate_input(i)
        M, N = input.shape
        res = main.main(None, {"S":S}, {illusion_name: input})[illusion_name]
        #{"c_ON": c_ON, "c_OFF": c_OFF, "l_ON": l_ON, "l_OFF": l_OFF, "M_ON": M_ON, "M_OFF": M_OFF}
        c_ON, c_OFF, l_ON, l_OFF, M_ON, M_OFF, LBD_h, LBD_v, GBD_h, GBD_v, R_h, R_v, bright = \
            res["c_ON"], res["c_OFF"], res["l_ON"], res["l_OFF"], res["M_ON"], res["M_OFF"], \
            res["LBD_h"], res["LBD_v"], res["GBD_h"], res["GBD_v"], res["R_h"], res["R_v"], res["bright"]

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
            plot3(save_path, input, bright, cut_height, N + S)


# Plot first part of results:
def plot1(save_path, c_ON, c_OFF, l_ON, l_OFF, M_ON, M_OFF):
    cmap = 'coolwarm'
    plt.figure(figsize=(15, 15))
    plt.subplot(321)
    plt.imshow(c_ON, cmap=cmap)
    plt.axis('off')
    plt.title('ON network: contrast')
    plt.clim(-c_ON.max(), c_ON.max())
    plt.colorbar()

    plt.subplot(322)
    plt.imshow(c_OFF, cmap=cmap)
    plt.axis('off')
    plt.title('OFF network: contrast')
    plt.clim(-c_OFF.max(), c_OFF.max())
    plt.colorbar()

    plt.subplot(323)
    plt.imshow(l_ON, cmap=cmap)
    plt.axis('off')
    plt.title('ON network: luminance')
    plt.clim(-l_ON.max(), l_ON.max())
    plt.colorbar()

    plt.subplot(324)
    plt.imshow(l_OFF, cmap=cmap)
    plt.axis('off')
    plt.title('OFF network: luminance')
    plt.clim(-l_OFF.max(), l_OFF.max())
    plt.colorbar()

    plt.subplot(325)
    plt.imshow(M_ON, cmap=cmap)
    plt.axis('off')
    plt.title('ON network: filled')
    plt.clim(-M_ON.max(), M_ON.max())
    plt.colorbar()

    plt.subplot(326)
    plt.imshow(M_OFF, cmap=cmap)
    plt.axis('off')
    plt.title('OFF network: filled')
    plt.clim(-M_OFF.max(), M_OFF.max())
    plt.colorbar()
    plt.savefig(save_path + '1.png')
    plt.close()


# Plot second part of results:
def plot2(save_path, LBD_h, LBD_v, GBD_h, GBD_v, R_h, R_v):
    cmap = 'coolwarm'
    plt.figure(figsize=(15, 15))
    plt.subplot(321)
    plt.imshow(LBD_h, cmap=cmap)
    plt.axis('off')
    plt.title('Local boundaries')
    plt.clim(-LBD_h.max(), LBD_h.max())
    plt.colorbar()

    plt.subplot(322)
    plt.imshow(LBD_v, cmap=cmap)
    plt.axis('off')
    plt.title('Local boundaries')
    plt.clim(-LBD_v.max(), LBD_v.max())
    plt.colorbar()

    plt.subplot(323)
    plt.imshow(GBD_h, cmap=cmap)
    plt.axis('off')
    plt.title('Global boundaries')
    plt.clim(-GBD_h.max(), GBD_h.max())
    plt.colorbar()

    plt.subplot(324)
    plt.imshow(GBD_v, cmap=cmap)
    plt.axis('off')
    plt.title('Global boundaries')
    plt.clim(-GBD_v.max(), GBD_v.max())
    plt.colorbar()

    plt.subplot(325)
    plt.imshow(R_h, cmap=cmap)
    plt.axis('off')
    plt.title('Integration')
    plt.clim(-R_h.max(), R_h.max())
    plt.colorbar()

    plt.subplot(326)
    plt.imshow(R_v, cmap=cmap)
    plt.axis('off')
    plt.title('Integration')
    plt.clim(-R_v.max(), R_v.max())
    plt.colorbar()
    plt.savefig(save_path + '2.png')
    plt.close()


# Plot third part of results:
def plot3(save_path, input_image, bright, cut_height, NS):
    plt.figure(figsize=(22, 6))
    plt.subplot(131)
    plt.imshow(input_image, cmap='gray')
    plt.title('Input stimulus')
    plt.colorbar()

    plt.subplot(132)
    plt.imshow(bright, cmap='coolwarm')
    plt.axhline(y=cut_height, color='k')
    plt.title('Brightness output')
    plt.clim(-bright.max(), bright.max())
    plt.colorbar()

    plt.subplot(133)
    x_ax = np.arange(0, np.size(bright, 1))
    plt.plot(x_ax, np.squeeze(bright[cut_height, :]), 'k')
    plt.ylim([-0.1, 1.1])
    plt.xlim([0, NS])
    plt.title('Cut through')
    plt.savefig(save_path + '3.png')
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
    im1 = plt.imshow(video1[:, :, 0], cmap='coolwarm', vmin=video1.min(), vmax=video1.max())
    plt.clim(-video1.max(), video1.max())
    plt.title('ON pathway: Frame 000')
    plt.axis('off')
    ax2 = plt.subplot(122)
    im2 = plt.imshow(video2[:, :, 0], cmap='coolwarm', vmin=video2.min(), vmax=video2.max())
    plt.clim(-video2.max(), video2.max())
    plt.title('OFF pathway: Frame 000')
    plt.axis('off')

    def animate(i):
        im1.set_array(video1[:, :, i])
        ax1.set_title(f'ON pathway: Frame {i:03d}')
        plt.axis('off')

        im2.set_array(video2[:, :, i])
        ax2.set_title(f'OFF pathway: Frame {i:03d}')
        plt.axis('off')

    n_frames = np.size(video1, 2)
    anim = FuncAnimation(fig, animate, frames=n_frames)
    anim.save('%s.gif' % fname, writer='imagemagick', fps=10)
    plt.close()


run_demo()