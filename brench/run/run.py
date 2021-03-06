import os
from brench.utils import load_dict, save_raw_model_output


def run(
    models,
    stimuli,
    evaluate_each=None,
    evaluate_all=None,
    outputs_dir=None,
    load=False,
    save=True,
):
    if load:
        assert outputs_dir is not None
        print(f"Loading outputs from {outputs_dir}")
    if save:
        assert outputs_dir is not None
        print(f"Saving outputs to {outputs_dir}")

    for model in models:
        for stim_name, stim_func in stimuli.items():
            print(f"Model {model['name']} on {stim_name}:")

            # Check for existing file
            if load:
                pickle_name = f"{model['name']}-{stim_name}.pickle"
                if (
                    (outputs_dir / "raw").exists()
                ) and pickle_name in os.listdir(outputs_dir / "raw"):
                    print(f"  found {pickle_name}.")
                    load = load_dict(outputs_dir / "raw" / pickle_name)
                    stim = load["stim"]
                    model_output = load["model_output"]
                else:
                    print(f"  no {pickle_name} found -- running")
                    # Run
                    stim = stim_func()
                    adapter = model["model_func"]
                    model_output = adapter(model["params"], stim.img)
            else:
                print(f"  running")
                # Run
                stim = stim_func()
                adapter = model["model_func"]
                model_output = adapter(model["params"], stim.img)

            # Save raw model outputs
            if save:
                pickle_name = f"{model['name']}-{stim_name}.pickle"
                print(f"  saving to {pickle_name}")
                save_raw_model_output(
                    {"model_output": model_output, "stim": stim},
                    outputs_dir / "raw" / pickle_name,
                )

            if evaluate_each is not None:
                print("  evaluating:")
                evaluate_each(
                    model["name"], stim_name, model_output, stim, outputs_dir
                )

            print("  done.")

    if evaluate_all is not None:
        evaluate_all(outputs_dir)
