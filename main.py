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
from fitting_view import FittingView
from docking_view import DockingView
from load_save_view import LoadSaveView

view = ViewManager()

view_dict = {
    View.GALAXY: GalaxyView(),
    View.SOLAR: SolarView(),
    View.PLANET: PlanetView(),
    View.FITTING: FittingView(),
    View.DOCKING: DockingView(),
    View.LOAD_SAVE: LoadSaveView()
}

view.setup_views(view_dict, View.GALAXY)

#view.solve()

view.run()

sys.exit()