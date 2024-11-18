#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 19:20:56 2024

@author: steve
"""

import math
from pygame.math import Vector2
import pandas as pd

import constants as const

planet_type_data = pd.read_csv('./data/planet_types.csv', index_col=0) 

    
class Planet():
    
    def __init__(self, name, r, p, planet_type, size, system):
        self.name = name
        self.r = r
        self.p = p
        self.planet_type = planet_type
        self.size = size
        self.color = planet_type_data[planet_type].color
        self.system = system
        self.xy = Vector2(const.screen_center.x - math.cos(p)*r,  const.screen_center.y - math.sin(p)*r)
        
        self.resources = {}
        
        #for i in range(0, random.randint(1, len(planet_resourses[planet_type]))):
        #    
        #    resource = planet_resourses[planet_type][i]
        #
        #    amount = random.randint(1, 10) * resource_mult[resource]
        #    self.resources[resource] = amount
            
    def description(self):
        return self.name