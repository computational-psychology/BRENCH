import stimuli

case1 = {
    "models": [
        {
            "name": "domijan2015",
            "model": None,
            "package": "domijan2015",
            "params": {"S": 20}
        },
    ],
    "stimuli": {
            "benary_cross": stimuli.illusions.benary_cross.domijan2015(),
        }
}

case2 = {
    "models": [
        {
            "name": "domijan2015",
            "model": None,
            "package": "domijan2015",
            "params": {"S": 20}
        },
    ],
    "stimuli": {
            "benary_cross": stimuli.illusions.benary_cross.domijan2015(),
            "dungeon": stimuli.illusions.dungeon.dungeon_illusion(),
            "todorovic": stimuli.illusions.todorovic.domijan2015()
    }
}

case3 = {
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
        },
    ],
    "stimuli": {
            "benary_cross": stimuli.illusions.benary_cross.domijan2015(),
            "dungeon": stimuli.illusions.dungeon.dungeon_illusion(),
            "todorovic": stimuli.illusions.todorovic.domijan2015()

    }
}