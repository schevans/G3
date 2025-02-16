#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 12:54:41 2025

@author: steve
"""

import utils
from bullet import Bullet


weapons_data = utils.csv_loader('./data/weapons.csv')

class Weapons():

    def __init__(self):
        
        self.data = weapons_data
        
        self.selected_weapon = 'lasers'
        
        self.ammo = {}
        
    def select(self, selection):
        pass
    
    def fire(self, selected_weapon):
        
        # if have_ammo:
        return Bullet(self.data[selected_weapon])
    
    def draw_icons(self):
        pass
        # icons