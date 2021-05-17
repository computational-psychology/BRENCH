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
        "dungeon": stimuli.papers_stimuli.domijan2015.dungeon(),
        "todorovic": stimuli.papers_stimuli.domijan2015.todorovic(),
        "benary_cross": stimuli.illusions.benary_cross.domijan2015(),
    }
}
