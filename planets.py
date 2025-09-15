#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 19:20:56 2024

@author: steve
"""

import pygame
import math
from pygame.math import Vector2
import json
  
import constants as const
import my_random
from planetary_textures import PlanetaryTextures


with open('./data/planet_types.json', 'r' ) as f:
    planet_type_data = json.load(f)

    
MINING_HIT_COUNTER = 20
PLANET_VIEW_RADIUS_MULT = 8
UMBRA_COLOR = ( 0, 0, 0, 128)

planetary_textures = PlanetaryTextures()

class Planet():
    
    def __init__(self, name, r, p, planet_type, size, system, station):
        self.name = name
        self.r = r
        self.p = p
        self.planet_type = planet_type
        self.size = size
        self.color1 = pygame.Color(planet_type_data[planet_type]['color1'])
        self.color2 = pygame.Color(planet_type_data[planet_type]['color2'])
        self.system = system
        self.station = station
        
        self.xy = Vector2(const.screen_center.x - math.cos(p)*r,  const.screen_center.y - math.sin(p)*r)
        self.planet_view_r = self.size * PLANET_VIEW_RADIUS_MULT
        
        self.atmos_color = self.color1
        if self.planet_type in ['rocky', 'earth-like']:
            self.atmos_color = self.color2
        
        self.resources = {}
        self.mining_hit_counter = MINING_HIT_COUNTER
        self.mining_can = {}
        for resource in const.initial_planetary_resources:
            self.resources[resource] = int(const.initial_planetary_resources[resource] *  my_random.my_random())
                
        self.resources_max = sum(self.resources.values())
        
        (self.image, self.small_image) = (None, None)
        self.shadow_surface = pygame.Surface((const.screen_width,const.screen_height), pygame.SRCALPHA)
        self.spin = 0

            
    def description(self, scanner_lvl):
        
        retval = self.name
        
        if scanner_lvl >= const.ScanTarget.PLANET_TYPES:
            retval += ', ' + self.planet_type.capitalize()
        
        if scanner_lvl >= const.ScanTarget.PLANETARY_RESOURCES:
            retval += ', resouces: ' +  str(int(sum(self.resources.values())))          
        
        return retval

                
    def object_type(self):
        return "Planet"
    
    def mine(self, bullet):
        
        retval = None
        
        mining_hit = bullet.shield_damage + bullet.armour_damage

        if sum(self.resources.values()) >= mining_hit:
            for i in range(int(mining_hit)):
                
                available_resources = [k for k in self.resources.keys() if self.resources[k] > 0]
                resource = my_random.my_choices(available_resources)[0]
                               
                if resource in self.mining_can:
                    self.mining_can[resource] += 1
                else:
                    self.mining_can[resource] = 1
                                    
                self.resources[resource] -= 1
                                
            self.mining_hit_counter -= mining_hit
            
            
            if self.mining_hit_counter <= 0:
                self.mining_hit_counter = MINING_HIT_COUNTER
                retval = self.mining_can.copy()
                self.mining_can = {}
            
        else:
            if sum(self.mining_can.values()):
                retval = self.mining_can.copy()
                self.mining_can = {}    
                for key in self.resources:
                    self.resources[key] = 0
            
        return retval
    
    def update(self):
        # defer planet gen 'till needed for perf
        if not self.image:
            (self.image, self.small_image) = planetary_textures.get_image(self)
            
        self.image.angle_deg = self.spin
        self.spin += 0.3
                
    def planet_view_draw(self, screen):
        
        pygame.draw.circle(screen, self.atmos_color, const.screen_center, self.planet_view_r, 3)

        # defer planet gen 'till needed for perf
        if not self.image:
            (self.image, self.small_image) = planetary_textures.get_image(self)
        self.image.draw(screen)
        
        
        
        self.shadow_surface.fill((0,0,0,0))
        theta = self.p + math.pi/2
        r = self.planet_view_r
        
        umbra_overhang = 2
        umbra1 = (const.screen_center[0]+math.cos(theta)*(r+umbra_overhang), const.screen_center[1]+math.sin(theta)*(r+umbra_overhang))
        umbra2 = (const.screen_center[0]-math.cos(theta)*(r+umbra_overhang), const.screen_center[1]-math.sin(theta)*(r+umbra_overhang))
        
        extent = const.screen_width / 2
        extent1 = (umbra1[0]+math.cos(theta+math.pi/2)*extent, umbra1[1]+math.sin(theta+math.pi/2)*extent)
        extent2 = (umbra2[0]+math.cos(theta+math.pi/2)*extent, umbra2[1]+math.sin(theta+math.pi/2)*extent)
        
        pygame.draw.polygon(self.shadow_surface, UMBRA_COLOR, (umbra1, umbra2, extent2, extent1))
        screen.blit(self.shadow_surface, (0,0))
        
    def solar_view_draw(self, screen):
        # defer planet gen 'till needed for perf
        if not self.small_image:
            (self.image, self.small_image) = planetary_textures.get_image(self)
           
        pygame.draw.circle(screen, 'gray', const.screen_center, self.r, 1)
        self.small_image.draw(screen)
        





