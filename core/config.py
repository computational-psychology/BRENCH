import stimuli


config = {
    "models": [
        {
            "name": "domijan2015",
            "model": None,
            "package" : "domijan2015",
            "params": {"S":20}
        },
       {
            "name": "multyscale_ODOGBM1999",
            "model": "ODOG_BM1999",
            "package" : "multyscale",
            "params": {"visextent": (-16, 16, -16, 16)}

        },
        {
            "name": "multyscale_LODOG_RHS2007",
            "model": "LODOG_RHS2007",
            "package" : "multyscale",
            "params": {"visextent": (-16, 16, -16, 16)}
        },
        {
            "name": "multyscale_FLODOG_RHS2007",
            "model": "FLODOG_RHS2007",
            "package" : "multyscale",
            "params": {"visextent": (-16, 16, -16, 16)}
        }
        ],

    "stimuli": {
        "RHS2007_WE_thick": stimuli.papers_stimuli.RHS2007.WE_thick(),
        "RHS2007_WE_circular": stimuli.papers_stimuli.RHS2007.WE_circular1(),
        "benary_cross": stimuli.illusions.benary_cross.domijan2015(),
    }
}
