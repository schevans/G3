#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 19:09:24 2024

@author: steve
"""
import utils
import constants as const

ship_systems_data = utils.csv_loader('./data/ship_systems.csv')
ship_systems_upgrade_data = utils.csv_loader('./data/ship_systems_upgrade.csv')


class ShipSystem():
    
    def __init__(self, name, level):
        self.name = name
        self.level = level
        
        self.data = ship_systems_data[name]
        
        if name not in ship_systems_upgrade_data:
            raise Exception('System ' + name + ' not added to /data/ship_systems_upgrade.csv') 
            
        self.upgrade = ship_systems_upgrade_data[name]

    def get_upgrade_cost(self, level):
        
        text = ''
        for key in self.upgrade:      
            text += (key + ': ' + str(self.upgrade[key] * (level+1) * const.upgrade_mult))
            if list(self.upgrade)[-1] != key:
                text += ' '
                
        return text


class Fit():
    

    
    def __init__(self, fit):
        self.fit = fit
        
        self.system_names = ship_systems_data.keys()
        
        if len(fit) != len(self.system_names):
            raise Exception('Fit string ' + fit + ' different length to ship_systems_data.keys()' )
        
        count = 0
        self.systems = {}
        for system in self.system_names:
            self.systems[system] = ShipSystem(system, self.fit[count])
            count += 1
        
        