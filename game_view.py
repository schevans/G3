#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 18:55:32 2024

@author: steve
"""
import pygame

import systems
import utils
import constants as const 





class GameView():
       
    
    def __init__(self, screen, ships):
        self.screen = screen
        self.ships = ships

        self.font = pygame.font.SysFont('Comic Sans MS', 22)
        self.mobs = []
        self.master_timer = 1
        
    def process_inputs(self):
        pass
        
    def update(self):
        
        for mob in self.mobs:
            if mob.name == 'Hero' or self.ships[0].is_moving():
                mob.update()
        
    def draw(self):
        
        self.screen.fill('black') 
        
        utils.draw_stars(self.screen)
        

    def draw_objects(self):
        
        for mob in self.mobs:
            mob.draw(self.screen)


    
    



        
