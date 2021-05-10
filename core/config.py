import multyscale
import stimuli
import os
import sys

domijan_dir = os.path.abspath(__file__ + "/../..")
sys.path.append(domijan_dir)
from domijan2015.main import main as domijan

config = {
    "models": [
        {
            "name": "domijan2015",
            "model": None,
            "main" : domijan,
           "params": {"S":20}
        },
       {
            "name": "multyscale_ODOGBM1999",
            "model": multyscale.models.ODOG_BM1999,
            "main" : multyscale.main.main,
            "params": {"visextent": (-16, 16, -16,16)}

        },
        {
            "name": "multyscale_LODOG_RHS2007",
            "model": multyscale.models.LODOG_RHS2007,
            "main": multyscale.main.main,
            "params": {"visextent": (-16, 16, -16,16)}
        },
        {
            "name": "multyscale_FLODOG_RHS2007",
            "model": multyscale.models.FLODOG_RHS2007,
            "main": multyscale.main.main,
            "params": {"visextent": (-16, 16, -16,16)}
        }
        ],

    "stimuli": {
        "RHS2007_WE_thick": stimuli.papers_stimuli.RHS2007.WE_thick(),
        "RHS2007_WE_circular": stimuli.papers_stimuli.RHS2007.WE_circular1(),
        "benary_cross": stimuli.illusions.benary_cross.domijan2015(),
    }
}

