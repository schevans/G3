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



BAR_SCALE = 25
LOCK_RADIUS = 15

hit_color = pygame.Color('orangered')
HIT_FLASH_INTERVAL = 100 # ms

AI_DITHER = 1000  #ms
AI_MIN = 250 # ms
AI_ACCELERATION = 0.3
AI_MINE_SEP = 30 # degrees behind
AI_RANGE_SEP = 20

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
        self.in_combat = False
        self.ai_target = None
        self.ai_timer = Timer()
        self.cap_timer = Timer()
        self.dmg_timer = Timer()
        
        self.planetary_mass = planet.mass
        self.planet_view_r = planet.planet_view_r
        
        self.w = math.sqrt(const.G*self.planetary_mass/math.pow(r, 3)) 

        
    def update(self):
        
        if self.acceleration:
            self.r += self.acceleration
            self.image = self.image_flying
        else:
            self.image = self.image_still 
            
        self.p += self.w
        self.w = math.sqrt(const.G*self.planetary_mass/math.pow(self.r, 3)) 
        
        self.xy[0] = const.screen_center.x - math.cos(self.p)*self.r
        self.xy[1] = const.screen_center.y - math.sin(self.p)*self.r
        
        if self.cap_timer.get_next_second():
            extra_cap = self.fit.systems['capacitor'].add_value(self.fit('reactor'))
            self.fit.systems['shield'].add_value(extra_cap)
            
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
        
        if self.is_current:
            self.draw_minifig(screen, surface)
            
    def shoot(self):
        return self.weapons.fire(self, self.locked_target)


    def hit(self, shield_damage, armour_damage):
        
        self.in_combat = True
        
        if self.fit('shield') >= shield_damage:
            self.fit.systems['shield'].value -= shield_damage
        elif self.fit('shield') > 0:
            ratio = (shield_damage - self.fit('shield')) / shield_damage
            self.fit.systems['shield'].value = 0
            self.fit.systems['armour'].value -= armour_damage * ratio
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


    def do_ai(self, mobs):     

        bullet = None        
        
        if self.is_current:
            self.locked_target = None
            return None
        
        # get targets
        targets = [mob for mob in mobs if mob.object_type() == 'Ship' and mob.is_alive and mob.liege != self.liege]
        
        #targets = [target for target in targets if target.name != 'Hero']       # TEMP TEMP ****   [dev_level 5??]
        
        # select target
        if len(targets) == 0:
            return bullet
        elif len(targets) == 1:
            self.ai_target = targets[0]
        else:
            
            self.ai_target = min(targets, key=lambda x:self.xy.distance_to(x.xy))
            
            # is lockable?
            targets = [target for target in targets if unobstructed_view(self.xy, target.xy, const.screen_center, self.planet_view_r)]
            if len(targets) != 0:
                self.ai_target = min(targets, key=lambda x:self.xy.distance_to(x.xy))
                
            # is behind? (moar shootable 'cause relative velocity)
            targets = [target for target in targets if math.pi - (target.p - self.p) % (2*math.pi) < 0]
            if len(targets) != 0:
               self.ai_target = min(targets, key=lambda x:self.xy.distance_to(x.xy))           

        self.locked_target = self.ai_target

               
        # select weapon, check range and fire
        in_range = True 
        if self.locked_target and self.ai_timer.get_next_ms_interval(AI_MIN + (AI_DITHER * my_random.my_random())):

            if abs(self.r - self.locked_target.r) < const.weapon_hit_radius and (self.locked_target.p - self.p) % (2*math.pi) > (2*math.pi) - math.radians(AI_MINE_SEP): 
                self.weapons.selected_weapon = ('mine')
            elif self.xy.distance_to(self.locked_target.xy) <= self.weapons.data['torpedo']['range'] * self.fit('wep range'):
                self.weapons.selected_weapon = ('torpedo')
            elif self.xy.distance_to(self.locked_target.xy) <= self.weapons.data['rocket']['range'] * self.fit('wep range'):
                self.weapons.selected_weapon = ('rocket')
            else:
                in_range = False
    
            if in_range:
                bullet = self.shoot()
        
        
        near_hemisphere =  abs(math.pi - (self.locked_target.p - self.p) % (2*math.pi)) > math.pi/2 

        if abs(self.r -self.ai_target.r) > AI_RANGE_SEP:
        
            if near_hemisphere:
                if self.r < self.ai_target.r:
                   self.acceleration = AI_ACCELERATION * const.acc_over_speed * self.fit.speed()
                else:
                   self.acceleration = -AI_ACCELERATION * const.acc_over_speed * self.fit.speed()
            else:
                if self.r > self.ai_target.r:
                   self.acceleration = AI_ACCELERATION * const.acc_over_speed * self.fit.speed()
                else:
                   self.acceleration = -AI_ACCELERATION * const.acc_over_speed * self.fit.speed()
        else:
            self.acceleration = 0
            
    
        return bullet


    def check_lock(self):
        if self.locked_target:
            if not unobstructed_view(self.xy, self.locked_target.xy, const.screen_center, self.planet_view_r):
                self.locked_target = None
        

    def is_hostile(self):
        return self.liege == const.hostile_capital or self.in_combat




