#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 17:46:52 2024

@author: steve
"""

import sys

from game_view import ViewManager, View
from galaxy_view import GalaxyView
from solar_view import SolarView
from planet_view import PlanetView



view = ViewManager()

view_dict = {
    View.GALAXY: GalaxyView(),
    View.SOLAR: SolarView(),
    View.PLANET: PlanetView()
}

view.setup_views(view_dict, View.GALAXY)

view.run()

sys.exit()