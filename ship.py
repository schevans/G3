#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 17:58:02 2024

@author: steve
"""

import pygame

import pandas as pd

import point
import rotatable_image
import utils

class Ship():
        
    def __init__(self, xy, is_npc):
        self.xy = point.Point(xy)
        self.is_npc = is_npc
                
        ship_systems_data = pd.read_csv('./data/ship_systems.csv', index_col=0)     # FIXME multiple reads
        self.shield = utils.MaxableAmount(float(ship_systems_data['0'].shield))
        self.armour = utils.MaxableAmount(float(ship_systems_data['0'].armour))
        self.capacitor = utils.MaxableAmount(float(ship_systems_data['0'].capacitor))
        
        self.speed = int(ship_systems_data['0'].engine)
        self.reactor = float(ship_systems_data['0'].reactor)
        
        self.is_alive = True
        self.heading = 0
        self.destination = self.xy

        self.image_still = rotatable_image.RotatableImage(self.xy, pygame.image.load('./graphics/Ship2.png'))
        self.image_flying = rotatable_image.RotatableImage(self.xy, pygame.image.load('./graphics/Ship2_flying.png'))
        

    def update(self):
        
        self.image_still.update(self.xy, self.heading)
    
    def draw(self, screen):
        
        self.image_still.draw(screen)
    
        pygame.draw.circle(screen, 'black', self.xy(), 1)
    
        
        
        
        
        
        
        
        