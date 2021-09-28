import domijan2015


def main(params, stim):
    """
    stim: 2D numpy array
    """
    S = params["S"]

    # Normalize stimulus between 1. and 9.
    stim = (stim - stim.min()) / (stim.max() - stim.min()) * (9.0 - 1.0) + 1.0
    output = domijan2015.main.main(stimulus, S)
    output["image"] = domijan2015.utils.remove_surround(
        output["image"], size=int(S / 2)
    )

    return output
