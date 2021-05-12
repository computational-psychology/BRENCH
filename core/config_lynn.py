import multyscale
import stimuli
import os
import sys

domijan_dir = os.path.abspath(__file__ + "/../..")
sys.path.append(domijan_dir)
import domijan2015.main

config = {
    "stimuli": {
        "RHS2007_WE_thick": stimuli.papers_stimuli.RHS2007.WE_thick(),
        "RHS2007_WE_circular": stimuli.papers_stimuli.RHS2007.WE_circular1(),
        "benary_cross": stimuli.illusions.benary_cross.domijan2015(),
    },

    "models": [
        {
            "name": "domijan2015",
            "model": domijan2015.main,
            "params": {"S": 20}
        },
        {
            "name": "odog1999",
            "model": multyscale.models.ODOG_BM1999.main,
            "params": {"visextent": (-16, 16, -16, 16)}
        },
        {
            "name": "lodog2007",
            "model": multyscale.models.LODOG_RHS2007.main,
            "main": multyscale.main.main,
            "params": {"visextent": (-16, 16, -16, 16)}
        },
        {
            "name": "flodog2007",
            "model": multyscale.models.FLODOG_RHS2007.main,
            "params": {"visextent": (-16, 16, -16, 16)}
        }
        ]
}
