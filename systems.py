#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 19:10:48 2024

@author: steve
"""
import my_random
from pygame.math import Vector2
from pygame import Color
import math
import pandas as pd

import constants as const
import planets
import utils
from stations import Station

STAR_SIZE_MIN = 3
STAR_SIZE_MAX = 8
STAR_SPACING = 40
STAR_TEMPERATURES = [(155,176,255), (146, 181, 255), (170, 191, 255), (162, 192, 255), (202, 215, 255), (213, 224, 255), (248, 247, 255), (249, 245, 255), (255, 244, 234), (255, 237, 227), (255, 210, 161), (255, 218, 181), (255, 204, 111), (255, 181, 108)] 
STAR_TEMP_FREQS = [3, 3, 12, 12, 60, 60, 300, 300, 700, 700, 1200, 1200, 70000, 70000]
STAR_TEMP_FREQS = [3, 3, 12, 12, 20, 20, 30, 30, 70, 70, 120, 120, 700, 700]
HOME_STAR_SIZE = 10



syslist = []

star_names = pd.read_csv('./data/star_names.csv')
star_names = star_names.Name.tolist()

def init_systems(num_systems):
        
    # home system
    syslist.append(System(const.our_capital, const.home_xy, HOME_STAR_SIZE, const.species_color[const.our_capital], 'Home'))
    
    # capitals
    syslist.append(System(const.neutral_capital, get_random_sys_location(), my_random.my_randint(STAR_SIZE_MIN, STAR_SIZE_MAX), const.species_color[const.neutral_capital], 'Neutral')) # FIXME: Much redundancy
    syslist.append(System(const.friendly_capital, get_random_sys_location(), my_random.my_randint(STAR_SIZE_MIN, STAR_SIZE_MAX), const.species_color[const.friendly_capital], 'Friendly'))
    syslist.append(System(const.hostile_capital, get_random_sys_location(), my_random.my_randint(STAR_SIZE_MIN, STAR_SIZE_MAX), const.species_color[const.hostile_capital], 'Hostile'))
    
    for i in range(0,num_systems):
        
        name = star_names[my_random.my_randint(0, len(star_names)-1)]
        star_names.remove(name)
        
        randpos = get_random_sys_location()
        randr = my_random.my_randint(STAR_SIZE_MIN, STAR_SIZE_MAX)
        
        system_type = const.system_types[my_random.my_randint(0, len(const.system_types)-1)]
        color = utils.fade_color_to(my_random.my_choices(STAR_TEMPERATURES, weights=STAR_TEMP_FREQS, k = 1)[0], Color('white'), 0.6)
        system = System(name, randpos ,randr, color, system_type)
        
        syslist.append(system)
    

    
def get_random_sys_location():

    
    rand = Vector2(my_random.my_randint(1, const.screen_width), my_random.my_randint(1, const.screen_height) )
    
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

def pickle():
    
    data = {}
    for system in syslist:
        data[system.name] = {}
        for planet in system.planets:
            data[system.name][planet.name] = {}
            data[system.name][planet.name]['resources'] = planet.resources
            if planet.station:
                data[system.name][planet.name]['station'] = planet.station.resources
            
    return data


def unpickle(data):
    
     for system in syslist:
         for planet in system.planets:
             planet.resources = data[system.name][planet.name]['resources']
             if planet.station:
                 planet.station.resources = data[system.name][planet.name]['station']
                 
                 
class System():
    
    def __init__(self, name, xy, r, color, system_type):
        self.name = name
        self.xy = Vector2(xy)
        self.r = r
        self.color = color
        self.system_type = system_type
        self.planets = []
        
        for i in range(0, my_random.my_randint(1, 4)):
            r = utils.get_random_r(r, max(const.planet_size_freq), self.planets)            
            p =  math.radians(my_random.my_random() * 360)            
            planet_type = planets.planet_type_data.columns.values[my_random.my_randint(0,len(planets.planet_type_data.columns.values)-1)]
            size = const.planet_size_freq[my_random.my_randint(0,len(const.planet_size_freq)-1)]
            planet_name = self.name + ' ' + utils.numbers_to_roman(i)
            
            station = None 
            if self.system_type == 'Uninhabited' and i == 0:
                station = Station(planet_name, const.screen_height/4)
    
            if self.name == const.our_capital:
                if i == 0:
                    planet_type = 'earth-like'
            
            planet = planets.Planet(planet_name, r, p, planet_type, size, self, station)
            self.planets.append(planet)
    
    
    def description(self, scanner_lvl):
        
        retval = self.name

        if scanner_lvl >= 1:
            if self.name in const.species.values() and self.name != const.our_capital:
                retval += ' Homeworld: ' + self.system_type
            else:
                retval += ': ' + self.system_type
                
        if scanner_lvl >= 2:
            resources = 0
            for planet in self.planets:
                resources += int(sum(planet.resources.values()))
                
            retval += ', resources: ' + str(resources)
                
        return retval

                
    def object_type(self):
        return "System"



