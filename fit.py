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
        
        text = []
        for key in self.upgrade:      
            text.append(key.title() + ': ' + str(self.upgrade[key] * const.upgrade_cost_mults[level]))
                
        return text

    def upgrade_system(self):
        self.level += 1
        
        
        
class Fit():
    

    
    def __init__(self, fit):
        
        self.system_names = ship_systems_data.keys()
        
        if len(fit) != len(self.system_names):
            raise Exception('Fit string ' + fit + ' different length to ship_systems_data.keys()' )
        
        count = 0
        self.systems = {}
        for system_name in self.system_names:
            self.systems[system_name] = ShipSystem(system_name, int(fit[count]))
            count += 1
        
    def upgrade(self, system):
        self.systems[system].upgrade_system()

    def to_string(self):
        retval = ''
        for system_name in self.system_names:
            retval += str(self.systems[system_name].level)
            
        return retval
            

    def speed(self):
        return self.systems['engine'].data[str(self.systems['engine'].level)]
    
    def level(self, system_name):
        return self.systems[system_name].level
    
    def function(self, system_name, level):
        return self.systems[system_name].data[str(level)]
    
    def __call__(self, system_name):
        return self.systems[system_name].data[str(self.systems[system_name].level)]








