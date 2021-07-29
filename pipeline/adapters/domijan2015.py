import domijan2015


# Run the simulations for 12 brightness illusions:
def main(model, params, stimuli):
    # Model class is not used

    S = params["S"]
    outputs = {}
    for stimulus_name, stimulus_func in stimuli.items():
        stimulus = stimulus_func()
        print("Running stimulus", stimulus_name, ", model: domijan")
        print("Stimulus shape:", stimulus.img.shape, "\n")
        stim = stimulus.img

        # Normalize stimulus between 1. and 9.
        stim = (stim - stim.min()) / (stim.max() - stim.min()) * (9. - 1.) + 1.
        output = domijan2015.main.main(stim, S)
        output['image'] = domijan2015.utils.remove_surround(output['image'], size=int(S/2))
        outputs[stimulus_name] = output

    return outputs
