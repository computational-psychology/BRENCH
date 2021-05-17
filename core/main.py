import importlib

import adapters

def main(config_module='config', config_dict='config'):

    # These two lines allow dynamic loading of config dict based on the passed parameters
    config_module = importlib.import_module(config_module) # load config module
    config = getattr(config_module, config_dict) # load config dict from the config module

    outputs = {}
    for model in config["models"]:
        print("Running model " + model["name"])
        runner = eval(f"adapters.{model['package']}.main")
        outputs[model["name"]] = runner(model["model"], model["params"], config["stimuli"])
    return outputs

