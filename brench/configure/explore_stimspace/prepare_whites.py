import stimuli.illusions


# Function that returns white function with chosen parameters:
def create_white_func(this_freq, this_height, this_lum):
    # Constant parameters:
    total_height, total_width, ppd = (32,) * 3
    height, width = 12, 16
    padding_horizontal = (total_width - width) / 2
    padding_vertical = (total_height - height) / 2
    padding = (
        padding_vertical,
        padding_vertical,
        padding_horizontal,
        padding_horizontal,
    )

    # Create instantiation with selected parameters:
    stim_func = stimuli.illusions.whites.white(
                    shape=(12, 16),
                    ppd=ppd,
                    frequency=this_freq,
                    period="ignore",
                    target_indices=(2, -3),
                    target_height=this_height * height,
                    high=0.9,
                    low=0.1,
                    target=this_lum,
                    padding=padding,
                    padding_val=0.5,
                    )

    # Return stimulus with chosen parameters as function (needed for stimulus dictionary)
    return lambda: stim_func


# Function that returns dictionary of white functions covering the desired stimspace:
def create_white_funcs(grating_frequencies, target_heights, target_luminances):
    # Initiate dictionary for stimulus functions:
    stim_funcs = {}
    for freq in grating_frequencies:
        for height in target_heights:
            for lum in target_luminances:
                name = f"white_{freq}_{height}_{lum}"
                stim_funcs[name] = create_white_func(freq, height, lum)
    return stim_funcs
