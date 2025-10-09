#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 17:58:02 2024

@author: steve
"""

import pygame
from pygame.math import Vector2
import math

import rotatable_image
import utils
import constants as const 
import fit
from weapons import Weapons
import my_random

class Ship():
        

    def __init__(self, name, xy, system, planet, is_npc, fit_string=None, is_hero=False):
        self.name = name
        self.xy = Vector2(xy)
        self.system = system
        self.planet = planet
        self.is_npc = is_npc
        self.is_hero = is_hero

        self.fit = fit.Fit(fit_string)
        self.fuel_modifier = 1
        self.movement_points = const.base_movement_points
        
        if system:
            self.liege = const.species[system.system_type]
            self.color = const.species_color[self.liege]

            self.resources = {}
            for k, v in const.their_initial_resources.items():
                if k == 'laser':
                    self.resources[k] = v
                else:
                    self.resources[k] = int(v*my_random.my_random())
                    
            # harden neutrals
            if self.liege == const.neutral_capital:
                self.fit.upgrade('capacitor')
                self.fit.upgrade('reactor')
                self.fit.upgrade('wep dmg')
                self.fit.upgrade('wep range')
                    
        else:
            self.liege = const.our_capital
            self.color = pygame.Color('white')
            self.resources = const.our_initial_resources.copy()

        self.species = self.liege
        self.orig_color = self.color
        self.is_alive = True
        self.heading = 0
        self.destination = None
        self.is_current = False

        self.load_and_color_images()
        self.image = self.image_still
        
        self.weapons = Weapons()

        # dev mode
        if const.dev_mode and self.is_hero:
            self.fit.upgrade('engine')
            self.fit.upgrade('engine')
            self.fit.upgrade('engine')
            self.fit.upgrade('scanner')
            self.fit.upgrade('scanner')
            self.fit.upgrade('scanner')
            if const.dev_mode >= 2:
                self.resources = self.resources.fromkeys(self.resources, 999)
            else:
                self.resources = self.resources.fromkeys(self.resources, 70)
            self.resources['laser'] = math.inf

        self.galaxy_xy = self.xy.copy()

    def update(self):
        
        if self.destination:
            
            
            
            if self.xy.distance_to(self.destination.xy) <= self.fit.speed():
                # arrived
                self.xy = Vector2(self.destination.xy)
                self.heading = 0
                self.image = self.image_still
                if self.destination.object_type() == 'Planet':
                    self.planet = self.destination
                else:
                    self.system = self.destination
                    self.planet = None
            else:
                # still moving
                self.heading = utils.angle_between_points(self.xy ,self.destination.xy)
                self.image = self.image_flying
                
                self.xy.x -= math.sin(math.radians(self.heading)) * self.fit.speed()
                self.xy.y -= math.cos(math.radians(self.heading)) * self.fit.speed()
                
            
        
            
        self.image.update(self.xy, self.heading)
    
    def draw(self, screen):

        self.is_current_outline()        

        if self.destination:    
            pygame.draw.line(screen, self.color, self.xy, self.destination.xy, 1)

        self.image.draw(screen)


    def draw_minifig(self, screen, ship_surface):

        # pic
        ship_surface = pygame.transform.scale_by(ship_surface, 2)
        ship_surface_width, ship_surface_height = ship_surface.get_size()

        # name
        name_surface = utils.fonts[20].render(self.name, True, 'white')
        name_surface_width, name_surface_height = name_surface.get_size()

        # fit
        fit_surface = utils.fonts[20].render('[' + self.fit.to_string() + ']', True, 'white')
        fit_surface_width, fit_surface_height = fit_surface.get_size()

        # new surface
        minifig_surface = pygame.Surface((max(ship_surface_width, name_surface_width, fit_surface_width), (ship_surface_height + name_surface_height + fit_surface_height)), pygame.SRCALPHA)
        minifig_surface_width, minifig_surface_height = minifig_surface.get_size()

        # blits
        minifig_surface.blit(ship_surface, ((minifig_surface_width-ship_surface_width)/2, 0))
        minifig_surface.blit(name_surface, ((minifig_surface_width-name_surface_width)/2, ship_surface_height))
        minifig_surface.blit(fit_surface, ((minifig_surface_width-fit_surface_width)/2, ship_surface_height + fit_surface_height))
        screen.blit(minifig_surface, Vector2((const.screen_width - minifig_surface_width - 20), 20))

        
    def is_current_outline(self):
        if not self.is_npc:
            if self.is_current:
                 self.image.change_color(pygame.Color('black'), pygame.Color('red')) 
            else:
                self.image.change_color(pygame.Color('red'), pygame.Color('black'))  


    def is_moving(self):
        return self.destination and self.xy != self.destination.xy

    def jump_cost(self, destination):
        return self.xy.distance_to(destination.xy) / ( const.distance_per_fuel * self.fuel_modifier )
    
    def jump_range(self):
        return self.resources['fuel'] * const.distance_per_fuel * self.fuel_modifier 

    def can_jump(self, destination):
           distance = self.jump_cost(destination)
           return distance < self.resources['fuel']
        
        
    def reset_xy(self, xy):
        self.xy = Vector2(xy)
        self.destination = None
        self.image.update(self.xy, self.heading)
      

    def description(self, scanner_lvl):
        
        retval = ''
        if self.is_hero:
            retval = self.name
        else:
            if self.name in const.species_color.keys():
                retval = 'First Lord ' + self.name
            else:
                retval = 'Lord ' + self.name + ' (' + self.liege[0] +')'
            
        fit_str = ''
        if self.liege == const.our_capital:
            fit_str = ' [' + self.fit.to_string() + ']'
        else:
            if scanner_lvl == const.ScanTarget.FIT_AVE:
                fit_str = ' (' + self.fit.to_string_ave() + ')'
            elif scanner_lvl >= const.ScanTarget.FIT_DETAIL:
                fit_str = ' [' + self.fit.to_string() + ']'
                
        retval += fit_str
            
        return retval
        

    def object_type(self):
        return 'Ship'

    def can_upgrade(self, system):
        
        retval = True
        for resource in self.fit.systems[system].upgrade:
            if self.resources[resource] < self.fit.systems[system].get_upgrade_cost(self.fit.level(system)+1, resource):
                retval = False
                
        return retval
    
    def upgrade_system(self, system):
        self.fit.systems[system].upgrade_system()
        
        for resource in self.fit.systems[system].upgrade:
            self.resources[resource] -= self.fit.systems[system].get_upgrade_cost(self.fit.level(system), resource)
             
        if system =='engine':
            self.fuel_modifier = const.fuel_efficiency[self.fit.level(system)]
            
            
    def recruit(self):
        self.is_npc = False
        self.liege = const.our_capital

        # ensure allies have enough fuel to get about
        self.resources['fuel'] = const.our_initial_resources['fuel']
        
    def pickle(self):
        
        destination = [self.destination.object_type(), self.destination.name] if self.destination else None
        system = self.system.name if self.system else None
        planet = self.planet.name if self.planet else None
        
        data = [self.xy, system, planet, destination, self.resources, self.fit, self.weapons.pickle(), self.is_npc, self.liege, self.heading, self.is_alive, self.movement_points, self.is_current, self.galaxy_xy]
        
        return data


    def unpickle(self, syslist, data):
        
        self.xy = data[0]
        self.system = next((x for x in syslist if x.name == data[1]), None)
        self.planet = next(x for x in self.system.planets if x.name == data[2]) if self.system and data[2] else None
        
        self.destination = data[3]
        if self.destination:
            if self.destination[0] == 'System':
                self.destination = next(x for x in syslist if x.name == self.destination[1])
        
        self.resources = data[4]
        self.fit = data[5]
        self.weapons.unpickle(data[6])
        self.is_npc = data[7]
        self.liege = data[8]
        self.heading = data[9]
        self.is_alive = data[10]
        self.movement_points = data[11]
        self.is_current = data[12]
        self.galaxy_xy = data[13]
        
        self.load_and_color_images()
        
        self.image.update(self.xy, self.heading)


    def scanner_lvl(self):
        return self.fit.systems['scanner'].level

    def can_do_first_upgrade(self):
        
        for system in self.fit.systems:
            if self.can_upgrade(system):
                return True

        return False
    
    
    def load_and_color_images(self):
        
        ship_image_number = str(const.ship_image_number[self.species])
        self.image_still = rotatable_image.RotatableImage(self.xy, pygame.image.load('./graphics/Ship' + ship_image_number + '.png'))
        self.image_flying = rotatable_image.RotatableImage(self.xy, pygame.image.load('./graphics/Ship_flying' + ship_image_number + '.png'))
        
        if not self.is_hero:
            self.image_still.change_color(pygame.Color('white'), self.orig_color)
            self.image_flying.change_color(pygame.Color('white'), self.orig_color)



