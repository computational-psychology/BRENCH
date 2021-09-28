import multyscale


def main(params, stim):
    """
    model_name: String
    stim: 2D numpy array
    """
    visextent = params["visextent"]
    model = params["model"]
    shape = stim.shape
    model_object = eval(f"multyscale.models.{model}(shape, visextent)")
    output = {"image": model_object.apply(stim)}

    return output
