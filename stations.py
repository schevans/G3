#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 10 19:18:01 2025

@author: steve
"""
import math
import pygame
from pygame import Vector2

import constants as const
import rotatable_image

class Station():
    
    def __init__(self, planet_name, r):

        self.r = r
        self.planet_name = planet_name

        self.name = 'Sister\'s Station, ' + self.planet_name
        self.mass = 1000 # FIXME. Also check planet.planet_view_r
        self.w = math.sqrt(const.G*self.mass/math.pow(r, 3)) 
        self.p = ( math.pi * 2 )
        self.xy = Vector2(const.screen_center.x - math.cos(self.p)*self.r,  const.screen_center.y - math.sin(self.p)*self.r)
        self.is_alive = True
        
        self.resources = const.our_initial_resources.fromkeys(const.our_initial_resources, const.station_resources)

        self.image_still = rotatable_image.RotatableImage(self.xy, pygame.image.load('./graphics/station.png'))

        self.liege = const.neutral_capital # FIXME: Hack? Or genius?
        
    def update(self):
        
        self.p -= self.w
        self.w = math.sqrt(const.G*self.mass/math.pow(self.r, 3)) 
        
        self.xy[0] = const.screen_center.x - math.sin(self.p)*self.r
        self.xy[1] = const.screen_center.y - math.cos(self.p)*self.r

        self.image_still.update(self.xy, math.degrees(self.p))
        
        
    def draw(self, screen):
        
        self.image_still.draw(screen)
    
    def description(self, scanner_lvl):
        return self.name
    
    def object_type(self):
        return "Station"





