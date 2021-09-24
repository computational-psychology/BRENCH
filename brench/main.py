import os

from brench.utils import load_dict


def main(config_dict, evaluate, final, outputs_dir=None):
    for model in config_dict["models"]:
        for stim_name, stim_func in config_dict["stimuli"].items():
            pickle_name = f"{model['name']}-{stim_name}.pickle"
            if outputs_dir is not None and os.path.isdir(outputs_dir) and pickle_name in os.listdir(outputs_dir):
                load = load_dict(os.path.join(outputs_dir, pickle_name))
                stim = load['stim']
                model_output = load['model_output']
            else:
                stim = stim_func()
                print(f"Running model {model['name']} on {stim_name}")
                adapter = model["adapter"]
                model_output = adapter(model["params"], stim.img)
            evaluate(model['name'], stim_name, model_output, stim)
    final()