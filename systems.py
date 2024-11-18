#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 19:10:48 2024

@author: steve
"""
import random
import pygame
from pygame.math import Vector2
import math
import pandas as pd

import constants as const
import planets

import utils

STAR_SIZE_MIN = 3
STAR_SIZE_MAX = 8
STAR_SPACING = 40
STAR_TEMPERATURES = [(155,176,255), (146, 181, 255), (170, 191, 255), (162, 192, 255), (202, 215, 255), (213, 224, 255), (248, 247, 255), (249, 245, 255), (255, 244, 234), (255, 237, 227), (255, 210, 161), (255, 218, 181), (255, 204, 111), (255, 181, 108)] 
STAR_TEMP_FREQS = [3, 3, 12, 12, 60, 60, 300, 300, 700, 700, 1200, 1200, 70000, 70000]
STAR_TEMP_FREQS = [3, 3, 12, 12, 20, 20, 30, 30, 70, 70, 120, 120, 700, 700]
HOME_STAR_SIZE = 10

system_types = ['Uninhabited', 'Neutral', 'Friendly', 'Hostile']

syslist = []

star_names = pd.read_csv('./data/star_names.csv')
star_names = star_names.Name.tolist()

def init_systems(num_systems):
    
    #star_names = pd.read_csv('./data/star_names.csv')
    #star_names = star_names.Name.tolist()
    
    for i in range(0,num_systems):
        
        name = star_names[random.randint(0, len(star_names)-1)]
        star_names.remove(name)
        
        randpos = get_random_sys_location()
        randr = random.randint(STAR_SIZE_MIN, STAR_SIZE_MAX)
        
        system_type = system_types[random.randint(0, len(system_types)-1)]
        
        color = utils.whiten_a_bit(random.choices(STAR_TEMPERATURES, weights=STAR_TEMP_FREQS, k = 1)[0], 0.4)
        system = System(name, randpos ,randr, color, system_type)
        
        syslist.append(system)
    
    # home system
    syslist.append(System('Home', const.home, HOME_STAR_SIZE, pygame.Color('turquoise2'), 'Friendly'))
    
def get_random_sys_location():

    
    rand = Vector2(random.randint(1, const.screen_width), random.randint(1, const.screen_height) )
    
    # don't spawn by the edges of the screen
    if rand.x < STAR_SIZE_MAX or rand.x > const.screen_width - STAR_SIZE_MAX or rand.y < STAR_SIZE_MAX or rand.y > const.screen_height - STAR_SIZE_MAX:
        return get_random_sys_location()
    
    # don't spawn near existing systems
    for system in syslist:
        if rand.distance_to(system.xy) < STAR_SPACING:
            return get_random_sys_location()
        
    # not near bottom-left corner (our spawn point)
    if rand.x < const.free_space_in_corners and rand.y > const.screen_height - const.free_space_in_corners:
        return get_random_sys_location()
    
    # or top-right (home)
    if rand.x > const.screen_width - const.free_space_in_corners and rand.y > const.free_space_in_corners:
        return get_random_sys_location()
        
    return rand

def numbers_to_roman(i):
    if i == 1:
        return 'I'
    elif i == 2:
        return 'II'
    elif i == 3:
        return 'III'
    elif i == 4:
        return 'IV'

class System():
    
    def __init__(self, name, xy, r, color, system_type):
        self.name = name
        self.xy = Vector2(xy)
        self.r = r
        self.color = color
        self.system_type = system_type
        self.planets = []
        
        
        
        
        for i in range(0, random.randint(1, 4)):
            r = self.get_random_r()
            p =  math.radians(random.random() * 360)            
            planet_type = planets.planet_type_data.columns.values[random.randint(0,len(planets.planet_type_data.columns.values)-1)]
            size = const.planet_size_freq[random.randint(0,len(const.planet_size_freq)-1)]
            planet_name = self.name + ' ' + numbers_to_roman(i+1)
            planet = planets.Planet(planet_name, r, p, planet_type, size, self)
            self.planets.append(planet)
         

         
    def get_random_r(self):
        r = int(random.random() * ( const.screen_height/2 - 80 ) + 40)
        
        for planet in self.planets:
            if math.isclose(r, planet.r, abs_tol=20):
                return self.get_random_r()
        return r
    
    
    def description(self):
        return self.name + ': ' + self.system_type

                
    



