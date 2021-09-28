import multyscale


def main(model, params, stim):
    """
    model_name: String
    stim: 2D numpy array
    """

    # Parameterize model
    visextent = params["visextent"]
    shape = stim.shape

    # Create model object
    model_object = eval(f"multyscale.models.{model}(shape, visextent)")

    # Run model
    output = {"image": model_object.apply(stim)}

    return output
