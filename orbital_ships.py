#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 18:58:26 2024

@author: steve
"""
import math 
import pygame
from pygame.math import Vector2

from ships import Ship        
import constants as const

G = 1

BAR_SCALE = 25

red_fade = pygame.Color(207, 1, 0, 64)

class OrbitalShip(Ship):
    
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
            
        self.p += self.w
        self.w = math.sqrt(G*self.mass/math.pow(self.r, 3)) 
        
        self.xy = Vector2(const.screen_center.x - math.cos(self.p)*self.r,  const.screen_center.y - math.sin(self.p)*self.r)
        
        if self.timer.get_next_second():
            self.fit.systems['capacitor'].value += self.fit('reactor')
            
    def draw(self, screen):
        
        self.width, self.height = self.image.original_image.get_size()
        
        surface = pygame.Surface((self.width+10, self.height), pygame.SRCALPHA)

        surface.blit(self.image.original_image, (7, 0))
        
        scaled_val = self.fit('shield') / self.fit.maximum('shield') * BAR_SCALE
        pygame.draw.rect(surface,
                 'cyan',
                 [0,
                  self.height-scaled_val-5,
                  2,
                  scaled_val])
        
        scaled_val = self.fit('armour') / self.fit.maximum('armour') * BAR_SCALE
        pygame.draw.rect(surface,
                 'red',
                 [4,
                  self.height-scaled_val-5,
                  2,
                  scaled_val])
    
        scaled_val = self.fit('capacitor') / self.fit.maximum('capacitor') * BAR_SCALE
        pygame.draw.rect(surface,
                 'yellow',
                 [self.width+8,
                  self.height-scaled_val-5,
                  2,
                  scaled_val])
        
        reverse = 0
        if self.acceleration < 0:
            reverse = 180
        
        rotated_image = pygame.transform.rotate(surface, math.degrees(-self.p)+reverse)
        new_rect = rotated_image.get_rect(center = surface.get_rect(topleft = self.xy).center)
        
        screen.blit(rotated_image, (new_rect[0]-new_rect[2]/2, new_rect[1]-new_rect[3]/2))
        
        if self.target:
            pygame.draw.circle(screen, red_fade, self.target.xy, 20, 1)
            pygame.draw.line(screen, red_fade, self.xy, self.target.xy)


    def shoot(self):

        return self.weapons.fire(self, self.target)

    def hit(self):
        pass



