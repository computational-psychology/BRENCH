import importlib

import adapters

def main(config):
    outputs = {}
    for model in config["models"]:
        print("Running model " + model["name"])
        runner = eval(f"adapters.{model['package']}.main")
        outputs[model["name"]] = runner(model["model"], model["params"], config["stimuli"])
    return outputs

