
# Motivation

*BRENCH* is created to solve three big problems regarding the research of computational models of human brightness perception.

- Lack of comparison between different models
  - There are various models of human brightness perception with different proposed working mechanisms.
    However, there are very few comparsions betweeen these models which makes it hard to discern which working mechanisms are generally relevant.
- Testing models on wide variety of input stimuli
  - Most models of human brightness perception are tested only on a small subset of input stimuli.
    *BRENCH* aims to facilitate testing models on a wide spectrum of input stimuli and analysing the results.
- Lack of public implementations
  - For many models of human brightness perception public implementation is not available.
    By making *BRENCH* completely open source and providing implementations of some models by ourselves, we aim to solve this problem.

# Installation

To install *BRENCH* you simply need to clone this repository and run `pip install .` (or `pip3 install .`) inside this directory.
If you want to use the models and stimuli we provide, you should also install the packages implementing these:

- [stimuli](https://github.com/computational-psychology/stimuli)
- [multyscale](https://github.com/computational-psychology/multyscale)
- [domijan2015](https://github.com/computational-psychology/domijan2015)

# Overview

*BRENCH* is organized around 3 main steps in evaluating models:

- *Configure* which model(s) should be run on which stimuli, and how the output should be evaluatied
- *Run* each model on each stimuli
- *Evaluate* the output that has been produced.

The framework is configured around these steps, and thus the `brench` module contains the `configure`, `run` and `evaluate` submodules (as well as some general `utils`, and `adapters` for making the provided models fit the generalized interface)

## Configure

To use *BRENCH*, one needs to _configure_ which model(s) should be run on which stimuli.
This is done in two dictionaries (`models`, and `stimuli`) that are passed to `run()`.

### Stimuli

In principle, the image computable models of brightness perception of interest, can be run on any arbitrary input image.
These input images should be represented as `numpy.ndarray`s, of arbitrary size.
(TODO: should these be in a fixed range, e.g., [0,1]?)

In practice, we tend to generate input stimulus images using the `stimuli` package.
For now, each stimulus should be an object with (at least these) two attributes: `img` and `target_mask`.  
`img` needs to be a 2D floating point numpy array representing the stimulus itself.
`target_mask` isn't strictly necessary in case when user does not want to run any sort of evaluation of model outputs with *BRENCH*
(e.g., calculating the mean difference between the target areas in the output).
In case it is needed, it needs to be a 2D numpy array with same dimensions as `img`.
It should contain an integer mask where 0 are the non-target areas and each separate target area is an incremented integer
(i.e., first target area is 1, second target area is 2, etc.).

For each stimulus, there should be a function that generates it.
The stimuli dictionary configured to pass to `run`, then, contains these functions as values,
and a user-meaningful name as the key:

```python
stimuli = {
    "stim_one": stimulus_generating_function1,
    "my_stim": stimulus_generating_function2,

}
```

Users are welcome to use input images coming from other sources as long as they conform to the standard to the necessary interface.

### Models

In principle, *BRENCH* believes that running a model should be done through the interface of a single function,
which takes a `image` a `params` argument:

```python
model_output = model(params, image)
```

where `params` is a dictionary containing necessary configuration parameters for that model and
`image` is an image array.
The resulting `output` is a dictionary,
which can contain arbitrary keys and values
(depending on the type of output that the model produces),
but *must* contain an `image` key
holding a 2D numpy floating point array specifying the brightness estimate of the model for the stimulus.

```python
output = {"image": 2D_model_output_image_array,
    "my_output1": Any,
    "more_output": Any,
    ...
}
```

Configuring models, then, is done by provide a dictionary (or list of dicts),
with the `model_func`tion to run, the `params` to pass to that function,
and a user-relevant `name` to identify this model
*NOTE*: this `name` can be used to identify the model and its output,
and should *NOT* contain any dashes (`-`). Underscores are fine.

```python
models = [
    {
        "name": "my_model_with_param1",
        "model_func": my_model,
        "params": {"param_name": param_value},
    },
    ...
]
```

#### Adapters, and running your own model
Due to the fact that different models from different packages differ **dramatically** in the way they are run and the parameters they accept
(e.g., some are object-oriented, some are functionally programmed),
models may require an adapter in order to fit the interface described.

Models provided together with *BRENCH* are parts of various different packages, and come with such adapaters provided.
The code for these resides in `utils/adapters`, and imported as `brench.utils.adapters`.
Each model-family has one adapter module, and each model has one adapter function.
It is possible to use your custom models,
but you must ensure that it either fits the interface, or provide an adapter to do so.

If a user wants to run some custom models, which are not provided by default, that is very much possible.
First step is creating an adapter module and function inside the `utils/adapters` directory
Second step is adding that module inside the `__init__` file in the `utils/adapters` directory.
E.g., if a user wants to add package `foo`, they should
create a file called `foo.py` inside the `adapters` directory,
put the `foo_model(params, stim)` function inside that file
and then add `from .foo import foo_model as foo_model_func` in the `utils/adapters/__init__.py` file.
Then, they can configure the model as:

```python
from brench.utils.adapters import foo_model_func
models = [
    {
        "name": "foo_with_param",
        "model_func": foo_model_func,
        "params": {"param_name": param_value},
    },
    ...
]
```

### Configuration files

Configuration consists only of passing the relevant `models` and `stimuli` datastructures to `brench.run()`,
which can be done from anywhere as long as *BRENCH* is properly installed.
However, we recommend creating a configuration file, in which you specify these configuration elements, for increased clarity and reproducibility.

The [configure](BRENCH/configure/) directory contains several such configuration files.
Every config file is 'just' a python script, so depending on the use case it might have different structure.
However, the main structure is usually the same.

First the relevant parts are imported, such as the model/adapter, and the stimuli:

```python
    # Models
    from brench.utils.adapters import domijan2015

    # Stimuli
    import stimuli.papers.domijan2015 as domijan_stimuli
```

Then, the models and stimuli are configured:

```python
# Configure models:
models = [
    {
        "name": "domijan2015",
        "model_func": domijan2015,
        "params": {"S": 20},
    }
]

# Configure stimuli
stimuli = {
    "dungeon": domijan_stimuli.dungeon,
    "cube": domijan_stimuli.cube,
    "grating": domijan_stimuli.grating,
    "ring": domijan_stimuli.rings,
    "bullseye": domijan_stimuli.bullseye,
    "simultaneous_brightness_contrast": domijan_stimuli.simultaneous_brightness_contrast,
    "white": domijan_stimuli.white,
    "benary_cross": domijan_stimuli.benary,
    "todorovic": domijan_stimuli.todorovic,
    "checkerboard_contrast_contrast": domijan_stimuli.checkerboard_contrast_contrast,
    "checkerboard_contrast": domijan_stimuli.checkerboard,
    "checkerboard_contrast_extended": domijan_stimuli.checkerboard_extended,
}
```

Finally, the whole thing should be run!

```python
if __name__ == "__main__":
    import brench.run
    output = brench.run(models, stimuli)
```

More can of course be added to the configuration file;
particularly useful are ways to _evaluate_ and save outputs, this is addressed below.


## Run

The main `run()` function is in and of itself quite simple.
As an input it takes a configuration of models (list), and a configuration of stimuli (dictionary),
runs all the models on all the stimuli, and returns all the outputs.
User should generally never have to change anything inside this function.

```python
all_models_outputs = brench.run(models, stimuli)
```

The output of `run()` is a dictionary
with a key called `input_stimuli` and one key for each of the models that was run.
The `input_stimuli` key contains a dictionary of input stimuli together with their names.
Per model that was run, there is a key with the model name and the value paired with it is a dictionary.
That dictionary has one key for each stimulus with the stimulus name and the value paired with it is the output of that model for that stimulus.

```python
all_models_outputs = {
    "input_stimuli":{
        stimulus_name: stimulus
    },
    model_name: {
        stimulus_name: output,
        ...
    },
    ...
}
```

### Caching: saving and loading
**TODO: describe**

## Evaluate
**TODO: describe**

# Use cases

1. Replicate the published results
    - If you simply want to replicate results from some papers implemented by BRENCH, you have a very simple task to do.
      Just go to the [configs](BRENCH/configs/) directory, find the paper you'd like to replicate and run the `config.py` inside it.
      Once the script is done, you should see the output files in the same directory. If you need the output in some other format, feel free to
      edit the `evaluate()` function inside the config file.

2. Cross-evaluation
    - In case you want to run a model from one of the implemented papers on some stimuli from another implemented model, your task is still quite simple.
      You should create a new config file that should be a copy of the config file of the paper you want to run
      (e.g., if you want to run `ODOG` model from *Robinson, Hammon and de Sa (2007)* paper, you would copy this [config.py](BRENCH/configs/RHS2007/config.py)).
      Next step is removing the models from the models list that you are not interested in. Afterwards, find the `config.py` with the stimuli you want to use
      (e.g., if you want to use stimuli from *Domijan 2015* paper you would use this [config.py](BRENCH/configs/domijan2015/config.py)).
      Copy all the stimuli you need and simply paste them instead of the original stimuli in the `config.py` you copied in the beginning.
      Finally, run your new `config.py` and that's it!

3. Testing new models
    - This use case follows the same logic as the last two. If you want to test new parametrization of some of the implemented models,
    you can simply copy the `config.py` and change the parameters in the models list. In case you want to test a model that is not provided
      with BRENCH, first read `Models and adapters` section and implement an adapter function for your model. Afterwards, simply create a new `config.py`
      where you can specify your model and the stimuli you need and then run it.

4. Testing new stimuli
    - If you want to test new stimuli on some of the existing models, simply create a `config.py` where you will specify the said model and the stimuli you need.
   If the stimuli you need is part of the `stimuli` package, than you can simply specify the function inside stimuli list. In case your stimulus comes from some other source,
      you can still use it with BRENCH. Read the `Stimuli` section to see the parameters that each stimulus needs to have.
      [Here](BRENCH/configs/ECVP21_poster/) you can see an example of how `adelson_checkershadow` was addeed to the config outside of the `stimuli` package.
