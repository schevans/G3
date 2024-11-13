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
import systems

class Ship():
        
    def __init__(self, name, xy, system, planet, is_npc):
        self.name = name
        self.location = utils.Location(Vector2(xy), system, planet)
        self.xy = self.location.galaxy_xy
        self.is_npc = is_npc

        ship_systems_data = pd.read_csv('./data/ship_systems.csv', index_col=0)     # FIXME multiple reads
        self.shield = utils.MaxableAmount(float(ship_systems_data['0'].shield))
        self.armour = utils.MaxableAmount(float(ship_systems_data['0'].armour))
        self.capacitor = utils.MaxableAmount(float(ship_systems_data['0'].capacitor))
        
        self.speed = int(ship_systems_data['0'].engine)
        self.reactor = float(ship_systems_data['0'].reactor)

        self.resources = const.initial_resources
        
        self.is_alive = True
        self.heading = 0
        self.destination = self.xy

        self.image_still = rotatable_image.RotatableImage(self.xy, pygame.image.load('./graphics/Ship.png'))
        self.image_flying = rotatable_image.RotatableImage(self.xy, pygame.image.load('./graphics/Ship_flying.png'))
        self.image = self.image_still

    def update(self):
        
        if self.is_moving():
            self.heading = utils.angle_between_points(self.xy ,self.destination)
            self.image = self.image_flying
            
            self.xy.x -= math.sin(math.radians(self.heading)) * self.speed
            self.xy.y -= math.cos(math.radians(self.heading)) * self.speed
            self.location.galaxy_xy = self.xy
        else:
            self.heading = 0
            self.image = self.image_still
            
        
        self.image.update(self.xy, self.heading)
    
    def draw(self, screen):
        
        self.image.draw(screen)

    
    
    def is_moving(self):
        if self.xy.distance_to(self.destination) < self.speed:
            self.destination = self.xy
            #self.location.system = systems.find_system_at(self.xy)
            return False
        else:
            return True
        
        
    def can_jump(self, destination):
           distance = self.xy.distance_to(destination)
           return distance < self.resources['fuel']
        
        
    def reset_xy(self, xy):
        self.xy = Vector2(xy)
        self.destination = self.xy
        