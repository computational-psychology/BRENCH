import multyscale

def main(model, params, stimuli):
    """
    model_name: String
    stimuli: {stimulus_name: stimulus_nparray}
    """
    visextent = params["visextent"]
    used_models = {}
    outputs = {}
    for stimulus_name, stimulus_func in stimuli.items():
        stimulus = stimulus_func()
        print("Running stimulus", stimulus_name, ", model:", model)
        print("Stimulus shape:", stimulus.img.shape, "\n")
        shape = stimulus.img.shape
        if shape not in used_models:
            model_object = eval(f"multyscale.models.{model}(shape, visextent)")
            used_models[shape] = model_object
        else:
            model_object = used_models[shape]

        # Return the output of the model applied on the stimulus
        outputs[stimulus_name] = {"image": model_object.apply(stimulus.img)}

    return outputs
