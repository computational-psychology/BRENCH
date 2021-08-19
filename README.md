# Motivation
*BrENCH* is created to solve three big problems regarding the research of computational models of human brightness perception.
- Lack of comparison between different models
    - There are various models of human brightness perception with different proposed working mechanisms.
    However, there are very few comparsions betweeen these models which makes it hard to discern which working mechanisms are generally relevant.
- Testing models on wide variety of input stimuli
    - Most models of human brightness perception are tested only on a small subset of input stimuli.
    *BrENCH* aims to facilitate testing models on a wide spectrum of input stimuli and analysing the results.
- Lack of public implementations
    - For many models of human brightness perception public implementation is not available.
    By making *BrENCH* completely open source and providing implementations of some models by ourselves, we aim to solve this problem.


# Installation
To install *BrENCH* you simply need to clone this repository and run `pip install .` (or `pip3 install .`) inside this directory.
If you want to use the configuration files we provide, you should also install the packages implementing the models used as well as the stimuli package:
* [stimuli](https://www.google.com)
* [multyscale](https://www.google.com)
* [domijan2015](https://www.google.com)


# Overview
*BrENCH itself has 3 main elements (main function, adapters, postprocessing module and config files) and depends on input stimuli and *an* implementation of a model of human brightness perception.



## Stimuli
By default, the way to generate the pipeline stimuli is using the `stimuli` package. Users are welcome to use stimuli 
coming from other sources as long as they conform to the standard. The only requirement is for stimuli to conform to the necessary interface.
Each stimulus should be an object with (at least these) two attributes: `img` and `target_mask`.  
`img` needs to be a 2D floating point numpy array representing the stimulus itself. `target_mask` isn't strictly necessary in case when
user does not want to run any sort of postprocessing calculations with *BrENCH* (e.g., calculating the mean difference between the target areas in the output).
In case it is needed, it needs to be a 2D numpy array with same dimensions as `img`. It should contain an integer mask where 0 are the non-target areas and each separate target area is an incremented integer
(i.e., first target area is 1, second target area is 2, etc.). For each stimulus, there should be a function that generates it.
This function is then referenced inside the config file (see lower in this README for more info).


## Models and adapters
Models provided together with BrENCH are parts of various different packages. It is possible to use your custom models, but it is a bit trickier than with the stimuli.  
Due to the fact that different models from different packages differ **dramatically** in the way they are run, and the parameters they accept, 
each package requires an interface in order to be able to work with the pipeline. This interface takes form of a `main()` function 
inside one of the modules in `adapters` directory. Each model has one adapter module and one `main()` function. 
Each `main` function has to accept three parameters: `model`, `params` and `stimuli`. 
`model` is a string specifying which model from that package needs to be run, 
`params` is a dictionary containing necessary configuration parameters for that model and 
`stimuli` is a dictionary of the form: `{"stimulus name": stimulus_func}` containing one or more stimuli (note that the value here is not the stimulus itself, but a reference to the function returing the stimuli) . 
The main function then takes care of doing whatever it takes to run this model for these input stimuli and returns the result to the pipeline. 
The result needs to be a dictionary where each key is a stimulus name and value is a dictionary containing the output of the model for that stimulus. 
This output can contain arbitrary keys and values (depending on the type of output that the model produces), but must contain an `image` key 
holding a 2D numpy floating point array specifying the brightness estimate of that model for that input stimulus. 
```python
output = {
    stimulus_name: {"image": model_output}, 
}
```

If a user wants to run some custom models, which are not provided by default, that is very much possible.  
First step is creating an adapter module inside the `adapter` directory the `main()` function as described above. 
Second step is adding that module inside the `__init__` file in the `adapters` directory. E.g., if a user wants to add package `foo`, they should
create a file called `foo.py` inside the `adapters` directory, put the `main()` function inside that file and then add `from . import foo` in the `__init__.py`
file in the adapters directory.


## main function
Main function is in and ofitself quite simple. As an input it takes in a config dictionary (more on that in the next section),
runs all the models with stimuli as specified in the config dictionary and returns all the outputs. User should generally never have to change anything inside this function.
The output of the function is a dictionary with one key called `input_stimuli` and one key for each of the run models. The `input_stimuli` key
contains a dictionary of input stimuli together with their names. Per model that was run, there is a key with the model name and the value paired with it is a dictionary.
That dictionary has one key for each stimulus with the stimulus name and the value paired with it is the output of that model for that stimulus.
```python
outputs = {
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

## Configs
The `configs` directory is where users can specify their config files. Each config file should be in its separate directory. Every config file
is 'just' a python script, so depending on the use case it might have different structure. However, the main structure is usually the same.
First comes the list of models. It should be in the following format:
```python
models = [
        {
            "name": model_name,
            "runner": reference to the main adapter function,
            "model": name of the model to run (depends on the runner function),
            "params": {param_name: param_value},
        },
    ...
```
After that comes the list of stimuli in the following format:
```python
stimuli = {
            "stim_name": stimulus_generating_function,
        ...
}
```
Finally both of those are put togeter in one dictionary:
```python
config_dict = {"models": models, "stimuli": stimuli}
```

After that comes the definition of the run function which in its simplest form looks like this:
```python
def run():
    res = main.run_model(config_dict)
    return res
```

Next part is optional and consist of the `evaluate()` function. Over here the results from the `run()` function are processed.
As an example one might want to plot them, show in table or calculate mean difference between the target areas. It might look like this:
```python
def evaluate(pipeline_dict):
    res = calculate_targets_means(pipeline_dict)
    plot_outputs(res, output_filename=output_filename + ".png")
    table = create_RHS_table(res, "output.csv", normalized=True)
```

Finally, the whole thing should be run!
```python
if __name__ == "__main__":
    res = run()
    evaluate(res)
```

For examples of config files (with some more complexity) check the [configs](brench/configs/) directory.


## Use cases

1. Replicate the published results
    - If you simply want to replicate results from some papers implemented by BrENCH, you have a very simple task to do. 
      Just go to the [configs](brench/configs/) directory, find the paper you'd like to replicate and run the `config.py` inside it.
      Once the script is done, you should see the output files in the same directory. If you need the output in some other format, feel free to
      edit the `evaluate()` function inside the config file.
      

2. Cross-evaluation 
    - In case you want to run a model from one of the implemented papers on some stimuli from another implemented model, your task is still quite simple. 
      You should create a new config file that should be a copy of the config file of the paper you want to run 
      (e.g., if you want to run `ODOG` model from *Robinson, Hammon and de Sa (2007)* paper, you would copy this [config.py](brench/configs/RHS2007/config.py)).
      Next step is removing the models from the models list that you are not interested in. Afterwards, find the `config.py` with the stimuli you want to use
      (e.g., if you want to use stimuli from *Domijan 2015* paper you would use this [config.py](brench/configs/domijan2015/config.py)).
      Copy all the stimuli you need and simply paste them instead of the original stimuli in the `config.py` you copied in the beginning.
      Finally, run your new `config.py` and that's it!
      

3. Testing new models
    - This use case follows the same logic as the last two. If you want to test new parametrization of some of the implemented models,
    you can simply copy the `config.py` and change the parameters in the models list. In case you want to test a model that is not provided
      with BrENCH, first read `Models and adapters` section and implement an adapter function for your model. Afterwards, simply create a new `config.py`
      where you can specify your model and the stimuli you need and then run it.
      

4. Testing new stimuli
    - If you want to test new stimuli on some of the existing models, simply create a `config.py` where you will specify the said model and the stimuli you need.
   If the stimuli you need is part of the `stimuli` package, than you can simply specify the function inside stimuli list. In case your stimulus comes from some other source,
      you can still use it with BrENCH. Read the `Stimuli` section to see the parameters that each stimulus needs to have.
      [Here](brench/configs/ECVP21_poster/) you can see an example of how `adelson_checkershadow` was addeed to the config outside of the `stimuli` package.




