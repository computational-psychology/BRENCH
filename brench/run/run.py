import os
from brench.utils import load_dict, save_raw_model_output


def run(config_dict, evaluate, final, outputs_dir=None, load=False, save=True):
    if load:
        assert outputs_dir is not None
        print(f"Loading outputs from {outputs_dir}")
    if save:
        assert outputs_dir is not None
        print(f"Saving outputs to {outputs_dir}")

    for model in config_dict["models"]:
        for stim_name, stim_func in config_dict["stimuli"].items():
            print(f"Model {model['name']} on {stim_name}: ", end="")

            # Check for existing file
            if load and ((outputs_dir / "raw").exists()):
                pickle_name = f"{model['name']}-{stim_name}.pickle"
                if pickle_name in os.listdir(outputs_dir / "raw"):
                    print(f"found {pickle_name}.")
                    load = load_dict(outputs_dir / "raw" / pickle_name)
                    stim = load["stim"]
                    model_output = load["model_output"]
                else:
                    print(f"no {pickle_name} found -- running.")
                    # Run
                    stim = stim_func()
                    adapter = model["adapter"]
                    model_output = adapter(model["params"], stim.img)
            else:
                print("running.")
                # Run
                stim = stim_func()
                adapter = model["adapter"]
                model_output = adapter(model["params"], stim.img)

            # Save raw model outputs
            if save:
                save_raw_model_output(
                    {"model_output": model_output, "stim": stim},
                    outputs_dir
                    / "raw"
                    / f"{model['name']}-{stim_name}.pickle",
                )

            # print("Evaluating")
            evaluate(model["name"], stim_name, model_output, stim, outputs_dir)
    final(outputs_dir)
