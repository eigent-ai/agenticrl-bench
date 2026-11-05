"""Illuminant reference data and utilities."""

import json
import os

from colortemp.cct_to_xy import CCT_to_xy_CIE_D


_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "illuminants.json")


def _load_config():
    with open(_CONFIG_PATH, "r") as f:
        return json.load(f)


def d65_reference_xy():
    """Return the CIE xy chromaticity coordinates for the D65 illuminant.

    Reads the CCT from the illuminants configuration file and computes
    xy via the CIE D-series formula.

    Returns
    -------
    list of float
        [x, y] chromaticity coordinates for D65.
    """
    config = _load_config()
    cct = config["D65"]["cct"]
    return CCT_to_xy_CIE_D(cct)
