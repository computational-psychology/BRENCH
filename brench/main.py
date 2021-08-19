from collections import OrderedDict

from brench import adapters

def run_model(config):
    outputs = OrderedDict()
    outputs["input_stimuli"] = config["stimuli"]
    for model in config["models"]:
        print("Running model " + model["name"])
        runner = model["runner"]
        outputs[model["name"]] = runner(model["model"], model["params"], config["stimuli"])
    return outputs
