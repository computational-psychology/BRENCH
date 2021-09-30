import stimuli.illusions


# Function that returns checkerboard function with chosen parameters:
def create_checkerboard_func(this_bheight, this_bwidth, this_csize):
    # Constant parameters:
    total_height, total_width, ppd = (32,) * 3
    board_shape = (this_bheight, this_bwidth)
    check1, check2, target = 1, 0, 0.5
    target_row = this_bheight // 2
    target_col = 3
    extend = False

    # Create instantiation with selected parameters:
    stim_obj = stimuli.illusions.checkerboard_contrast(
                    ppd=ppd,
                    board_shape=board_shape,
                    check_size=this_csize,
                    targets_coords=((target_row, target_col), (target_row, -target_col)),
                    extend_targets=extend,
                    check1=check1,
                    check2=check2,
                    target=target
                )

    # Increase image and target mask size to total_height+total_width via padding:
    total_size_px = (total_height*ppd, total_width*ppd)
    stim_obj.img = stimuli.utils.pad_img_to_shape(stim_obj.img, total_size_px, val=0.5)
    stim_obj.target_mask = stimuli.utils.pad_img_to_shape(stim_obj.target_mask, total_size_px, val=0.0)

    # Return stimulus with chosen parameters as function (needed for stimulus dictionary)
    return lambda: stim_obj


# Function that returns dictionary of checkerboard functions covering the desired stimspace:
def create_checkerboard_funcs(board_heights, board_widths, check_sizes):
    # Initiate dictionary for stimulus functions:
    stim_funcs = {}
    for bheight in board_heights:
        for bwidth in board_widths:
            for csize in check_sizes:
                name = f"checkerboard_{bheight}_{bwidth}_{csize}"
                stim_funcs[name] = create_checkerboard_func(bheight, bwidth, csize)
    return stim_funcs
