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

        self.maximum = self.data[str(self.level)]
        self.value = self.maximum
        

    def get_upgrade_cost(self, level, resource):
        if level > 3:  # FIXME: Hack
            return 0.0
        else:
            return self.upgrade[resource] * const.upgrade_cost_mults[level]

    def get_upgrade_cost_str(self, level):
        
        text = []
        for key in self.upgrade:      
            text.append(key.title() + ': ' + str(self.get_upgrade_cost(level, key)))
                
        return text

    def upgrade_system(self):
        if self.level < 3:
            self.level += 1
            self.maximum = self.data[str(self.level)]
            self.value = self.maximum
        
        
    def add_value(self, value):
        
        remainder = self.value + value - self.maximum
        if remainder > 0:
            self.value = self.maximum
            return remainder
        else:
            self.value += value
            return 0

        
class Fit():
    

    
    def __init__(self, fit):
        
        self.system_names = list(ship_systems_data.keys())
        
        if not fit:
            fit = ''
            fit = fit.rjust(len(self.system_names), '0')

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
         
    def to_string_ave(self):
        retval = 0
        for system_name in self.system_names:
            retval += self.systems[system_name].level
            
        return str(retval/len(self.system_names))

    def speed(self):
        return self.systems['engine'].value
    
    def maximum(self, system_name):
        return self.systems[system_name].maximum
    
    def level(self, system_name):
        return self.systems[system_name].level
    
    def __call__(self, system_name):
        return self.systems[system_name].value








