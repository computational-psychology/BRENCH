# Load other configs
from brench.configure import Domijan2015_config, RHS2007_config

# Where does this config save, by default?
from pathlib import Path

output_dir = Path(__file__).parents[2] / "data" / "combined"


models = Domijan2015_config.models + RHS2007_config.models
stimuli = {**Domijan2015_config.stimuli, **RHS2007_config.stimuli}

# Run from the command-line
if __name__ == "__main__":
    import time
    import brench.run

    # If existent, load model outputs:
    load_pickle = True
    # Save model outputs and evaluation results:
    save_pickle = True

    start = time.time()

    # Run framework with specified config and evaluation functions:
    brench.run(
        models,
        stimuli,
        outputs_dir=output_dir,
        load=load_pickle,
        save=save_pickle,
    )

    stop = time.time()
    print(
        "All done! Elapsed time:"
        f" {((stop-start)/60):2.0f}m:{((stop-start) % 60):2.0f}s"
    )
