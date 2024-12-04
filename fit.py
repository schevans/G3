#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 19:09:24 2024

@author: steve
"""
import utils


ship_systems_data = utils.csv_loader('./data/ship_systems.csv')
ship_systems_upgrade_data = utils.csv_loader('./data/ship_systems_upgrade.csv')


class ShipSystem():
    
    def __init__(self, name, level):
        self.name = name
        self.level = level
        
        self.data = ship_systems_data[name]
        self.upgrade = ship_systems_upgrade_data[name]

        
 
    
    
    

class Fit():
    

    
    def __init__(self, fit):
        self.fit = fit
        
        