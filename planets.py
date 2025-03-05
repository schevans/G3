#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 19:20:56 2024

@author: steve
"""

import pygame
import math
from pygame.math import Vector2
import pandas as pd
import numpy as np # FIXME TEMP
temp_rng = np.random.RandomState()      # FIXME TEMP
  
import constants as const
import my_random
from planetary_textures import PlanetaryTextures

planet_type_data = pd.read_csv('./data/planet_types.csv', index_col=0) 

MINING_HIT_COUNTER = 10

PLANET_VIEW_RADIUS_MULT = 8

planetary_textures = PlanetaryTextures()

class Planet():
    
    def __init__(self, name, r, p, planet_type, size, system):
        self.name = name
        self.r = r
        self.p = p
        self.planet_type = planet_type
        self.size = size
        self.color1 = pygame.Color(planet_type_data[planet_type].color1)
        self.color2 = pygame.Color(planet_type_data[planet_type].color2)
        self.system = system
        self.xy = Vector2(const.screen_center.x - math.cos(p)*r,  const.screen_center.y - math.sin(p)*r)
        
        self.planet_view_r = self.size * PLANET_VIEW_RADIUS_MULT
        
        # FIXME: Temp - use my_random
        self.resources = {}
        self.mining_hit_counter = MINING_HIT_COUNTER
        self.mining_can = {}
        for resource in const.initial_planetary_resources:
            amount = int(const.initial_planetary_resources[resource] * temp_rng.random_sample())
            if amount:
                self.resources[resource] = amount
                
        self.resources_max = sum(self.resources.values())
        
        (self.image, self.small_image) = (None, None)

        self.spin = 0
            
    def description(self):
        return self.name + ', ' + self.planet_type.capitalize() + ', resouces: ' +  str(sum(self.resources.values()))

                
    def object_type(self):
        return "Planet"
    
    def mine(self, bullet):
        
        mining_hit = 1 #bullet.shield_damage + bullet.armour_damage
        
        for i in range(int(mining_hit)):
            if bool(self.resources):
                resource = my_random.my_choices(list(self.resources.keys()))[0]
                if resource in self.mining_can:
                    self.mining_can[resource] += 1
                else:
                    self.mining_can[resource] = 1
                                    
                self.resources[resource] -= 1
                if self.resources[resource] == 0:
                    del(self.resources[resource])
                            
        self.mining_hit_counter -= mining_hit
        
        retval = None
        if self.mining_hit_counter <= 0:
            self.mining_hit_counter = MINING_HIT_COUNTER
            retval = self.mining_can.copy()
            self.mining_can = {}
            
        return retval
    
    def update(self):
        # defer planet gen 'till needed for perf
        if not self.image:
            (self.image, self.small_image) = planetary_textures.get_image(self)
            
        self.image.angle_deg = self.spin
        self.spin += 0.3
                
    def planet_view_draw(self, screen):
        # defer planet gen 'till needed for perf
        if not self.image:
            (self.image, self.small_image) = planetary_textures.get_image(self)
        self.image.draw(screen)
        
    def solar_view_draw(self, screen):
        # defer planet gen 'till needed for perf
        if not self.small_image:
            (self.image, self.small_image) = planetary_textures.get_image(self)
           
        pygame.draw.circle(screen, 'gray', const.screen_center, self.r, 1)
        self.small_image.draw(screen)
        





