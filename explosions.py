#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 17:55:27 2025

@author: steve
"""

import pygame

class Explosion():
    
    
    def __init__(self, xy, size, speed):
        self.xy = xy
        self.speed = speed
        self.size = size
        
        self.timer = 0
        self.is_alive = True
        
    def update(self):
        
        self.timer += 1 * self.speed
        
        if self.timer >= self.size:
            self.is_alive = False  

            
    
    def draw(self, screen): 
        
        if self.is_alive: # TODO: Move to update()
            brightness = self.size / (self.size - self.timer)
            explo_color = tuple(int(x/brightness) for x in (255, 255, 255)) 
    
            pygame.draw.circle(screen, explo_color, self.xy, 4+self.timer)

    
    def object_type(self):
        return 'Explosion'



