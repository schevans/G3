#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 18:53:23 2024

@author: steve
"""

import pygame
from pygame.math import Vector2

import utils
import constants as const
from game_view import GameView
from gui import Label, Button



class DockingView(GameView):
    

    
    def __init__(self):
        GameView.__init__(self)   
   

    def cleanup(self):
        pass
        
    
    def startup(self, shared_dict):
        self.shared_dict = shared_dict
        self.current_ship = self.shared_dict['current_ship']
        self.other_ship = self.shared_dict['other_ship']
        
    def process_event(self, event):
             
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                self.next_view = (self.shared_dict['prev_view'], self.shared_dict)
            
        
    def update(self):
        
        pass
                 
    
    def draw_background(self, screen):
        GameView.draw(self, screen)
        
        current_ship_image = utils.scale_and_monochrome_ship_image(self.current_ship)
        other_ship_image = utils.scale_and_monochrome_ship_image(self.other_ship)
        
        width, height = current_ship_image.get_size()
        screen.blit(current_ship_image, (0, const.screen_height/2 - height/2 + 60))            
        
        width, height = other_ship_image.get_size()
        screen.blit(other_ship_image, (const.screen_width - width, const.screen_height/2 - height/2 + 60))    
        
        
    def draw(self, screen):

        self.draw_background(screen)
        


    







