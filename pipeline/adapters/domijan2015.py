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
        output = domijan2015.main.main(stimulus.img, S)
        output['image'] = domijan2015.utils.remove_surround(output['image'], size=int(S/2))
        outputs[stimulus_name] = output

    return outputs
