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
LOCK_RADIUS = 15

hit_color = pygame.Color('orangered')
HIT_FLASH_INTERVAL = 100 # ms

AI_DITHER = 1000  #ms
AI_MIN = 250 # ms
AI_ACCELERATION = 0.3

def unobstructed_view(xy1, xy2, cpt, r):
    
    if xy1.distance_to(cpt) > xy1.distance_to(xy2):
        return True
    else:
        return not line_intersects_circle(xy1, xy2, cpt, r)
            
def line_intersects_circle(xy1, xy2, cpt, r):
    
    x1 = xy1[0] - cpt[0]
    y1 = xy1[1] - cpt[1]
    x2 = xy2[0] - cpt[0]
    y2 = xy2[1] - cpt[1]
    
    dx = x2 - x1
    dy = y2 - y1
    dr = math.sqrt(dx*dx + dy*dy)
    D = x1 * y2 - x2 * y1
    discriminant = r*r*dr*dr - D*D

    return discriminant >= 0

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
        
        self.mass = 7000 / planet.size # FIXME. Also check planet.planet_view_r
        self.planet_view_r = planet.planet_view_r
        
        self.w = math.sqrt(G*self.mass/math.pow(r, 3)) 

        
    def update(self):
        
        if self.acceleration:
            self.r += self.acceleration
            self.image = self.image_flying
        else:
            self.image = self.image_still 
            
        self.p += self.w
        self.w = math.sqrt(G*self.mass/math.pow(self.r, 3)) 
        
        self.xy[0] = const.screen_center.x - math.cos(self.p)*self.r
        self.xy[1] = const.screen_center.y - math.sin(self.p)*self.r
        
        if self.cap_timer.get_next_second():
            self.fit.systems['capacitor'].value += self.fit('reactor')
            
        if self.locked_target and not self.locked_target.is_alive:
            self.locked_target = None
            
        if self.color != self.orig_color and self.dmg_timer.get_next_ms_interval(HIT_FLASH_INTERVAL):
            self.image_still.change_color(self.color, self.orig_color)
            self.image_flying.change_color(self.color, self.orig_color)
            self.color = self.orig_color

            
    def draw(self, screen):
        
        self.is_current_outline() 
        
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


    def shoot(self):
        return self.weapons.fire(self, self.locked_target)


    def hit(self, shield_damage, armour_damage):
        
        if self.fit('shield') >= shield_damage:
            self.fit.systems['shield'].value -= shield_damage
        elif self.fit('shield') > 0:
            ratio = (shield_damage - self.fit('shield')) / shield_damage
            self.fit.systems['shield'].value = 0
            self.fit.systems['armour'].value = armour_damage * ratio
        elif self.fit('armour') > armour_damage:
            self.fit.systems['armour'].value -= armour_damage
        else:
            self.is_alive = False
        
        self.image.change_color(self.color, hit_color)
        self.color = hit_color
        self.dmg_timer.get_next_ms_interval(HIT_FLASH_INTERVAL)


    def loot(self, lootbox):
        
        for resource in lootbox.resources:
            self.resources[resource] += lootbox.resources[resource]

        lootbox.is_alive = False
        
    def lock_target(self, xy, mobs):
        
        for mob in mobs:
            if mob.object_type() == 'Ship':
                if mob.xy.distance_to(xy) <= LOCK_RADIUS:
                    if unobstructed_view(self.xy, mob.xy, const.screen_center, self.planet_view_r):
                        self.locked_target = mob
                        if not self.is_current:
                            self.ai_target = self.locked_target 
                        else:
                            self.ai_target = None

    def do_ai(self, mobs):     

        bullet = None        

        is_ally = not self.is_npc and not self.is_current
        is_hostile = self.is_npc and self.is_hostile()

        if is_ally or is_hostile: 

            if not self.ai_target:
                enemies = []
                for enemy in mobs:
                    if enemy.object_type() == 'Ship' and enemy.is_alive and (( is_hostile and not enemy.is_npc) or (is_ally and enemy.is_npc)):
                        if unobstructed_view(self.xy, enemy.xy, const.screen_center, self.planet_view_r):
                            enemies.append(enemy)
                enemies.sort(key=lambda x: x.xy.distance_to(enemy.xy))
                if enemies:
                    self.ai_target = enemies[0]  
    
            if self.ai_target and not self.locked_target:
                if unobstructed_view(self.xy, self.ai_target.xy, const.screen_center, self.planet_view_r):
                    self.locked_target = self.ai_target        
         
            if self.locked_target:
                if self.locked_target.is_alive:
            
                    in_range = True            
        
                    if abs(self.r - self.locked_target.r) < const.weapon_hit_radius * 2 and self.p - self.locked_target.p > 0.3:
                        self.weapons.selected_weapon = ('mine')
                    elif self.xy.distance_to(self.locked_target.xy) <= self.weapons.data['torpedo']['range'] * self.fit('wep range'):
                        self.weapons.selected_weapon = ('torpedo')
                    elif self.xy.distance_to(self.locked_target.xy) <= self.weapons.data['rocket']['range'] * self.fit('wep range'):
                        self.weapons.selected_weapon = ('rocket')
                    else:
                        in_range = False        
            
                    if self.ai_timer.get_next_ms_interval(AI_MIN + (AI_DITHER * my_random.my_random())):
                        if in_range:
                            bullet = self.shoot()

                    if in_range:
                        # match enemy r
                        if abs(self.r - self.locked_target.r) > const.weapon_hit_radius:
                            self.acceleration = AI_ACCELERATION if self.r < self.locked_target.r else -AI_ACCELERATION
                        else:
                            self.acceleration = 0 
                    else:
                        # close on enemy - go lower if ahead and higher if behind
                        if self.p - self.locked_target.p > math.pi:
                            self.acceleration = AI_ACCELERATION
                        else:
                            self.acceleration = -AI_ACCELERATION
                            
                    
                else:
                    self.locked_target = None
                    self.ai_target = None
                    self.acceleration = 0


        return bullet


    def check_lock(self):
        if self.locked_target:
            if not unobstructed_view(self.xy, self.locked_target.xy, const.screen_center, self.planet_view_r):
                self.locked_target = None
        

    def is_hostile(self):
        return self.liege == const.hostile_capital




