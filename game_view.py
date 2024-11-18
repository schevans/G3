#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 18:55:32 2024

@author: steve
"""
import pygame
from pygame.math import Vector2

import utils
import constants as const

TEXT_OFFSET = 15

class GameView():
       
    
    def __init__(self, screen, current_ship, ships):
        self.screen = screen
        self.current_ship = current_ship 
        self.ships = ships

        self.myship = ships[0]
        self.myships = []
        for ship in ships:
            if not ship.is_npc:
                self.myships.append(ship)
        

        self.font = pygame.font.SysFont('Comic Sans MS', 22)
        self.mobs = []
        self.master_timer = 1
        self.threat_level = 3
        
        self.selected_item = None
        
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
        
        if self.selected_item:
            
            textbox_width = 0
            textbox_height = 0
            text_arr = self.get_mouse_text()
            for text in text_arr:
                size = self.font.size(text)
                textbox_width = textbox_width if size[0] < textbox_width else size[0]
                textbox_height += size[1]
                
            surface = pygame.Surface((textbox_width, textbox_height))
            
            for i in range(0, len(text_arr)):
                text_surface = self.font.render(text_arr[i], True, 'white', 'black')
                surface.blit(text_surface,  (0, size[1] * (i)))
        
            
            text_pos = self.selected_item.xy + (TEXT_OFFSET,TEXT_OFFSET)
            textbox_width, textbox_height = text_surface.get_size()

            if textbox_width > const.screen_width - text_pos[0]:
                text_pos = self.selected_item.xy + (-textbox_width - TEXT_OFFSET,TEXT_OFFSET)
            
            if textbox_height > const.screen_height - text_pos[1]:
                text_pos = self.selected_item.xy + (TEXT_OFFSET, -textbox_height - TEXT_OFFSET)
        
            self.screen.blit(surface, text_pos )

        
    
    



        
