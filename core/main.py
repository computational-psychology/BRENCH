from config import config


def main():
    outputs = {}
    for model in config["models"]:
        print("Running model " + model["name"])
        outputs[model["name"]] = model["main"](model["model"], model["params"], config["stimuli"])
    return outputs

main()