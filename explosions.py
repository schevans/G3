#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 17:55:27 2025

@author: steve
"""

import pygame

class Explosion():
    
    
    def __init__(self, xy, size, speed, resources):
        self.xy = xy
        self.speed = speed
        self.size = size
        self.resources = resources 
        
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

crate_image = pygame.image.load('./graphics/crate2.png')

class LootBox():
    
    def __init__(self, xy, resources):
        self.xy = xy
        self.resources = resources
        self.image = crate_image
        self.is_alive = True
        
    def update(self):
        pass
        # FIXME: Make lights blinky
            
    
    def draw(self, screen): 
        
        if self.is_alive:
            image_rect = self.image.get_rect()
            image_rect.center = self.xy
            screen.blit(self.image, image_rect )

    def description(self, scanner_lvl):
        retval = ['Loot Box:']
        
        for resource in self.resources:
            if resource != 'laser':
                retval.append(resource.capitalize() + ': ' + str(self.resources[resource]))
        
        return retval
        
        
    def object_type(self):
        return 'LootBox'   
