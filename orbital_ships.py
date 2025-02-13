#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 18:58:26 2024

@author: steve
"""
import math 
import pygame
from pygame.math import Vector2

import ships        
import constants as const

G = 1

class OrbitalShip(ships.Ship):
    
    def __init__(self, ship, planet, r, p ):
        
        
        self.__dict__.update(vars(ship))
        
        self.tmpship = ship   # FIXME: Better solution
       
        self.r = r
        self.p = p
        self.acceleration = 0
        self.xy = Vector2(const.screen_center.x - math.cos(self.p)*self.r,  const.screen_center.y - math.sin(self.p)*self.r)
        self.target = None    
        
        self.mass = 7000 / planet.size # FIXME
        
        self.w = math.sqrt(G*self.mass/math.pow(r, 3)) 

        
    def update(self):
        
        if self.acceleration:
            self.r += self.acceleration
            self.image = self.image_flying
        else:
            self.image = self.image_still 
        
        if self.acceleration < 0:
            self.image.update(self.xy, 180)
            
        self.p += self.w
        self.w = math.sqrt(G*self.mass/math.pow(self.r, 3)) 
        
        self.heading = math.degrees(-self.p)
        self.xy = Vector2(const.screen_center.x - math.cos(self.p)*self.r,  const.screen_center.y - math.sin(self.p)*self.r)
  
        reverse = 0
        if self.acceleration < 0:
            reverse = 180
            
        self.image.update(self.xy, self.heading+reverse)
    
    def draw(self, screen):
        
        self.tmpship.draw(screen)       # FIXME: Hmmm. Might be useful? Linked to mobs[0] in planet_view
        
        if self.target:
            pygame.draw.circle(screen, 'green', self.target.xy, 20, 2)





            
            