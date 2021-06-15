import stimuli


config_template = {
    "models": [
        {
            "name": "<User assigned name>>",
            "model": "<Name of the model to be run, can be found in the documentation of the package>",
            "package" : "<Package containing the model>",
            "params": "<Dictionary of model parameters, depends on the model>"
        },

        ],

    "stimuli": {
        "<User assigned stimulus name>": "<Stimulus array>",
    }
}


"""
This config dict will result in models ODOGBM1999 and domijan2015 both being run on two stimuli: 
WE_circular from RHS2007 paper and benary cross as used in domijan2015 paper
"""
config_example = {
    "models": [
        {
            "name": "domijan2015",
            "model": "",
            "package": "domijan2015",
            "params": {"S": 20}
        },
        {
            "name": "multyscale_ODOGBM1999",
            "model": "ODOG_BM1999",
            "package": "multyscale",
            "params": {"visextent": (-16, 16, -16, 16)}

        },
        ],

    "stimuli": {
        "RHS2007_WE_circular": stimuli.papers_stimuli.RHS2007.WE_circular1(), # Stimulus array
        "benary_cross": stimuli.illusions.benary_cross.domijan2015(),
    }
}

