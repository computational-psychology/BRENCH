import matplotlib.pyplot as plt

import stimuli
import utils

stimuli_illusions = {}
utils_illusions = {}
stimuli_illusions["dungeon_illusion"] = stimuli.illusions.dungeon.dungeon_illusion(n_cells=5, target_radius=1, cell_size=10, back=1.0, grid=9.0, target=5.0, double=True)
utils_illusions["dungeon_illusion"] = utils.generate_input(1)[0]
# there's one-off translation between the stimuli package and utils generated inputs

stimuli_illusions["cube_illusion"] = stimuli.illusions.cube.cube_illusion(n_cells=4, target_length=2, cell_size=10, cell_spacing=3, padding=5, occlusion_overlap=4, back=0., grid=1., target=.5, double=True)
utils_illusions["cube_illusion"] = utils.generate_input(2)[0]
# the dimensions of two outputs is totally different

stimuli_illusions["grating_illusion"] = stimuli.illusions.grating.grating_illusion(n_bars=5, target_length=1, bar_width=10, back=0., grid=1., target=0.5, double=True)
utils_illusions["grating_illusion"] = utils.generate_input(3)[0]

stimuli_illusions["ring_illusion"] = stimuli.illusions.rings.ring_pattern(n_rings=8, target_pos_l=4, target_pos_r=3, ring_width=5, padding=10, back=0., rings=1., target=.5, invert_rings=False, double=True)
utils_illusions["ring_illusion"] = utils.generate_input(4)[0]

stimuli_illusions["bullseye_illusion"] = stimuli.illusions.bullseye.bullseye_illusion(n_rings=8, ring_width=5, padding=10, back=0., rings=1., target=.5)
utils_illusions["bullseye_illusion"] = utils.generate_input(5)[0]

stimuli_illusions["SC_illusion"] = stimuli.illusions.sbc.simultaneous_brightness_contrast(input_size=100, target_size=20, left=1., right=0., target=.5)
utils_illusions["SC_illusion"] = utils.generate_input(6)[0]

#stimuli_illusions["white_illusion"] = stimuli.illusions.whites.white_illusion(100, 2, 10, invert=False, grid_lum=1, switch_polarity=False, width_howe=0, anderson_displacement=0)
#utils_illusions["white_illusion"] = utils.generate_input(7)[0]

stimuli_illusions["benary_cross"] = stimuli.illusions.benary_cross.benarys_cross(input_size=100, cross_thickness=20, padding=10, back=1., cross=0., target=.5)
utils_illusions["benary_cross"] = utils.generate_input(8)[0]

stimuli_illusions["todorovic_illusion"] = stimuli.illusions.todorovic.todorovic_illusion(input_size=100, target_size=40, spacing=5, padding=15, back=0., grid=1., target=.5, double=True)
utils_illusions["todorovic_illusion"] = utils.generate_input(9)[0]

#stimuli_illusions["contrast_illusion"] = utils.generate_input(10)[0]
#utils_illusions["contrast_illusion"] = utils.generate_input(10)[0]

stimuli_illusions["checkerboard_illusion"] = stimuli.illusions.checkerboard_sbc.checkerboard_contrast(n_checks=8, check_size=10, target1_coords=(3, 2), target2_coords=(5, 5), extend_targets=False, padding=10, check1=0., check2=1., target=.5)
utils_illusions["checkerboard_illusion"] = utils.generate_input(11)[0]

#stimuli_illusions["checkerboard_extended_illusion"] = stimuli.illusions.checkerboard_contrast_contrast.checkerboard_contrast_contrast_effect(n_checks=8, check_size=10, target_length=4, padding=10, check1=0., check2=1.,tau=.5, alpha=.5)
#utils_illusions["checkerboard_extended_illusion"] = utils.generate_input(12)[0]


N = len(stimuli_illusions)+5
plt.figure(figsize=(5,20))

for i, (name, illusion) in enumerate(stimuli_illusions.items()):
    plt.subplot(N, 2, 2*i+1)
    plt.title(name)
    plt.imshow(illusion)

    plt.subplot(N, 2, 2 * i + 2)
    plt.title(name)
    plt.imshow(utils_illusions[name])



plt.show()