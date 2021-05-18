import stimuli

config = {
    "models": [
        {
            "name": "domijan2015-S20",
            "model": None,
            "package": "domijan2015",
            "params": {"S": 20}
        },
        {
            "name": "domijan2015-S40",
            "model": None,
            "package": "domijan2015",
            "params": {"S": 40}
        },
        {
            "name": "multyscale LODOG_RHS2007",
            "model": "LODOG_RHS2007",
            "package" : "multyscale",
            "params": {"visextent": (-16, 16, -16, 16)}
        },
{
            "name": "multyscale FLODOG_RHS2007",
            "model": "FLODOG_RHS2007",
            "package" : "multyscale",
            "params": {"visextent": (-16, 16, -16, 16)}
        },
    ],
    "stimuli": {
            "benary_cross": stimuli.illusions.benary_cross.lynn_domijan2015(),
            "dungeon": stimuli.illusions.dungeon.dungeon_illusion(),
            "todorovic": stimuli.illusions.todorovic.lynn_domijan2015()
    }
}
