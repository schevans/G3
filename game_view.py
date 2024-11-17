#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 18:55:32 2024

@author: steve
"""
import pygame

import utils


class GameView():
       
    
    def __init__(self, screen, ships):
        self.screen = screen
        self.ships = ships

        self.myship = ships[0]
        self.current_ship = self.myship      
        self.myships = []
        for ship in ships:
            if not ship.is_npc:
                self.myships.append(ship)
        

        self.font = pygame.font.SysFont('Comic Sans MS', 22)
        self.mobs = []
        self.master_timer = 1
        self.threat_level = 3
        
    def process_inputs(self):
        pass
        
    def update(self):
        
        for mob in self.mobs:
            mob.update()
        
    def draw(self):
        
        self.screen.fill('black') 
        
        utils.draw_stars(self.screen)
        

    def draw_objects(self):
        
        for mob in self.mobs:
            mob.draw(self.screen)
            
        # selected ship
        pygame.draw.circle(self.screen, 'red', self.current_ship.xy, 3)


    
    



        
