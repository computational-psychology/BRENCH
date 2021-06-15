import domijan2015

# Run the simulations for 12 brightness illusions:
def main(model, params, stimuli):
    # Model class is not used

    S = params["S"]
    outputs = {}
    for stimulus_name, stimulus in stimuli.items():
        print("Running stimulus", stimulus_name)
        outputs[stimulus_name] = domijan2015.main.main(stimulus, S)

    return outputs
