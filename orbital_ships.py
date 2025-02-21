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
from timer import Timer
import my_random

G = 1

BAR_SCALE = 25

red_fade = pygame.Color(207, 1, 0, 64)

hit_color = pygame.Color('orangered')
HIT_FLASH_INTERVAL = 100 # ms

AI_DITHER = 1000  #ms
AI_MIN = 250 # ms

class OrbitalShip(Ship):
    
    def __init__(self, ship, planet, r, p ):
        
        
        self.__dict__.update(vars(ship))
        
        self.tmpship = ship   # FIXME: Better solution
       
        self.r = r
        self.p = p
        self.acceleration = 0
        self.xy = Vector2(const.screen_center.x - math.cos(self.p)*self.r,  const.screen_center.y - math.sin(self.p)*self.r)
        self.locked_target = None    
        self.ai_target = None
        self.ai_timer = Timer()
        self.cap_timer = Timer()
        self.dmg_timer = Timer()
        self.orig_color = self.color
        
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
        
        if self.cap_timer.get_next_second():
            self.fit.systems['capacitor'].value += self.fit('reactor')
            
        if self.locked_target and not self.locked_target.is_alive:
            self.locked_target = None
            
        if self.color != self.orig_color and self.dmg_timer.get_next_ms_interval(HIT_FLASH_INTERVAL):
            self.image_still.change_color(self.color, self.orig_color)
            self.color = self.orig_color
            
            
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
        
        if self.locked_target:
            pygame.draw.circle(screen, red_fade, self.locked_target.xy, 20, 1)
            pygame.draw.line(screen, red_fade, self.xy, self.locked_target.xy)


    def shoot(self):
        return self.weapons.fire(self, self.locked_target)


    def hit(self, bullet):
        
        if self.fit('shield') >= bullet.shield_damage:
            self.fit.systems['shield'].value -= bullet.shield_damage
        elif self.fit('shield') > 0:
            ratio = (bullet.shield_damage - self.fit('shield')) / bullet.shield_damage
            self.fit.systems['shield'].value = 0
            self.fit.systems['armour'].value = bullet.armour_damage * ratio
        elif self.fit('armour') > bullet.armour_damage:
            self.fit.systems['armour'].value -= bullet.armour_damage
        else:
            self.is_alive = False
        
        self.image_still.change_color(self.color, hit_color)
        self.color = hit_color
        self.dmg_timer.get_next_ms_interval(HIT_FLASH_INTERVAL)


    def loot(self, lootbox):
        
        for resource in lootbox.resources:
            self.resources[resource] += lootbox.resources[resource]

        lootbox.is_alive = False
        

    def do_ai(self):
        
        if self.locked_target.is_alive:
        
            if self.ai_timer.get_next_ms_interval(AI_MIN + (AI_DITHER * my_random.my_random())):
    
                if abs(self.r - self.locked_target.r) < const.weapon_hit_radius * 2:
                    if self.p - self.locked_target.p < 0.3:
                        self.weapons.select('5') # mine. FIXME
                elif self.xy.distance_to(self.locked_target.xy) <= self.weapons.data['torpedo']['range'] * self.fit('wep range'):
                    self.weapons.select('4') # torp. FIXME
                elif self.xy.distance_to(self.locked_target.xy) <= self.weapons.data['rocket']['range'] * self.fit('wep range'):
                    self.weapons.select('3') # rockets. FIXME
                else:
                    return None
                
                if self.locked_target:
                    bullet = self.shoot()
                    return bullet
        else:
            self.locked_target = None
            self.ai_target = None

            


