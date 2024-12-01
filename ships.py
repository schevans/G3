#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 17:58:02 2024

@author: steve
"""

import pygame
from pygame.math import Vector2
import pandas as pd
import math

import rotatable_image
import utils
import constants as const 



class Ship():
        
    def __init__(self, name, xy, system, planet, is_npc):
        self.name = name
        self.xy = Vector2(xy)
        self.system = system
        self.planet = planet
        self.is_npc = is_npc
        self.home_system = system
        
        if system:
            self.liege = const.species[system.system_type]
        else:
            self.liege = 'Hero'
        
        ship_systems_data = pd.read_csv('./data/ship_systems.csv', index_col=0)     # FIXME multiple reads
        self.shield = utils.MaxableAmount(float(ship_systems_data['0'].shield))
        self.armour = utils.MaxableAmount(float(ship_systems_data['0'].armour))
        self.capacitor = utils.MaxableAmount(float(ship_systems_data['0'].capacitor))
        
        self.speed = int(ship_systems_data['0'].engine)
        self.reactor = float(ship_systems_data['0'].reactor)

        self.resources = const.initial_resources
        
        self.is_alive = True
        self.heading = 0
        self.destination = None
        self.is_current = False

        self.image_still = rotatable_image.RotatableImage(self.xy, pygame.image.load('./graphics/Ship.png'))
        self.image_flying = rotatable_image.RotatableImage(self.xy, pygame.image.load('./graphics/Ship_flying.png'))
        
        if self.is_npc:
            self.image_still.change_color(pygame.Color('white'), const.species_color[self.liege])
            self.image_flying.change_color(pygame.Color('white'), const.species_color[self.liege])

        self.image = self.image_still
        
        self.resources = const.initial_resources

        # dev mode
        if self.name == 'Hero':
            self.speed = 7

    def update(self):
        
        
        if self.destination:
            
            if self.xy.distance_to(self.destination.xy) <= self.speed:
                # arrived
                self.xy = Vector2(self.destination.xy)
                self.heading = 0
                self.image = self.image_still
                if self.destination.item_type() == 'Planet':
                    self.planet = self.destination
                else:
                    self.system = self.destination
                    self.planet = None
            else:
                # still moving
                self.heading = utils.angle_between_points(self.xy ,self.destination.xy)
                self.image = self.image_flying
                
                self.xy.x -= math.sin(math.radians(self.heading)) * self.speed
                self.xy.y -= math.cos(math.radians(self.heading)) * self.speed

        if not self.is_npc:
            if self.is_current:
                 self.image.change_color(pygame.Color('black'), pygame.Color('red')) 
            else:
                self.image.change_color(pygame.Color('red'), pygame.Color('black')) 
            
        self.image.update(self.xy, self.heading)
    
    def draw(self, screen):

        self.image.draw(screen)

    
    def is_moving(self):
        return self.destination and self.xy != self.destination.xy


    def can_jump(self, destination):
           distance = self.xy.distance_to(destination.xy)
           return distance < self.resources['fuel']
        
        
    def reset_xy(self, xy):
        self.xy = Vector2(xy)
        self.destination = None
      

    def description(self):
        if self.name == 'Hero':
            return self.name
        else:
            return 'Lord ' + self.name + ', for ' + self.liege
        

    def item_type(self):
        return "Ship"











