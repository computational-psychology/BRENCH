import multyscale


def ODOG_RHS2007(params, stim):
    """
    model_name: String
    stim: 2D numpy array
    """

    # Parameterize model
    visextent = params["visextent"]
    shape = stim.shape

    # Create model object
    model_object = multyscale.models.ODOG_RHS2007(shape, visextent)

    # Run model
    output = {"image": model_object.apply(stim)}

    return output


def LODOG_RHS2007(params, stim):
    """
    model_name: String
    stim: 2D numpy array
    """

    # Parameterize model
    visextent = params["visextent"]
    shape = stim.shape

    # Create model object
    model_object = multyscale.models.LODOG_RHS2007(shape, visextent)

    # Run model
    output = {"image": model_object.apply(stim)}

    return output


def FLODOG_RHS2007(params, stim):
    """
    model_name: String
    stim: 2D numpy array
    """

    # Parameterize model
    visextent = params["visextent"]
    shape = stim.shape

    # Create model object
    model_object = multyscale.models.FLODOG_RHS2007(shape, visextent)

    # Run model
    output = {"image": model_object.apply(stim)}

    return output
