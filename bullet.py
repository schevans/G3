#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 17:14:47 2025

@author: steve
"""
import math

from rotatable_image import RotatableImage
import constants as const


def get_angle_to_target(xy1, xy2):
    distance =  xy1 - xy2
    return math.atan2(distance[0], distance[1])


class Bullet():
    
    def __init__(self, shooter, target, mousepos, image, data):
        
        self.xy = shooter.xy.copy()
        self.shooter_xy = shooter.xy
        self.target = target
        
        self.speed = data['speed'] * shooter.fit('wep range')
        self.shield_damage = data['shield_damage'] * shooter.fit('wep dmg')
        self.armour_damage = data['armour_damage'] * shooter.fit('wep dmg')
        self.homing = data['homing']
        self.range = data['range'] * shooter.fit('wep range')
        
        target_xy = target.xy if target else mousepos
        self.angle = get_angle_to_target(self.xy, target_xy)

        self.is_alive = True
        self.range_timer = 0
        self.is_armed = False

        self.rot_image = RotatableImage(self.xy, image)

    
    def update(self):


        if not self.is_armed and self.xy.distance_to(self.shooter_xy) > const.weapon_hit_radius:
            self.is_armed = True
        
        if self.range_timer >= self.range:
            self.is_alive = False
        else:
            self.range_timer += self.speed
            
            if self.homing:
                if self.xy.distance_to(self.target.xy) < const.weapon_hit_radius:
                    self.hit(self.target)
                else:
                    self.angle = get_angle_to_target(self.xy, self.target.xy)
            
            self.xy[0] -= math.sin(self.angle) * self.speed
            self.xy[1] -= math.cos(self.angle) * self.speed
            
            self.rot_image.update(self.xy, math.degrees(self.angle)+90)
     
    
    def draw(self, screen):
        
        if self.is_alive:
            self.rot_image.draw(screen)
            
    
    def object_type(self):
        return 'Bullet'
    
    
    def hit(self, mob):

        if self.is_armed:
            mob.hit(self.shield_damage, self.armour_damage)
            self.is_alive = False
            




