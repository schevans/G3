#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 18:43:09 2024

@author: steve
"""

import pygame
from pygame import Vector2

import utils

game_color = (255, 181, 108)
   
        
        
class Button():
    
    def __init__(self, xy, size, text, color, mouseover_text):
        self.xy = xy
        self.size = size
        self.text = text
        self.color = pygame.Color(color)
        self.mouseover_text = mouseover_text
        
        self.lighter_color = utils.whiten_a_bit(self.color, 0.5)
        self.darker_color = utils.fade_to_black(self.color, 1, 2)
        self.border_color = self.lighter_color
        self.button_color = self.color
        
        self.is_active = False
        self.is_disabled = False
        self.is_pressed = False
        self.surface =  pygame.Surface(size)

        
    def process_event(self, event):
        
        if self.is_active:
            self.is_pressed = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.is_pressed = True
                    print('Pressed')
                      
        
            if self.is_pressed:
                self.button_color = self.darker_color
                self.border_color = 'black'
            else:
                self.border_color = self.lighter_color
                self.button_color = self.color
            
    def update(self):
        
        if not self.is_disabled:
            self.is_active = False
            mousepos = pygame.mouse.get_pos()
            if pygame.Rect(self.xy, self.size).collidepoint(mousepos):
                self.button_color = self.lighter_color
                self.is_active = True
            else:
                self.button_color = self.color
        
        if self.is_disabled:
            self.button_color = self.darker_color
            self.border_color = self.darker_color
            

    def draw(self, screen):
        
        self.surface.fill(self.button_color)
        
        # border
        rect = self.surface.get_rect()
        pygame.draw.rect(self.surface, game_color, rect, 1)
        rect[0] += 1
        rect[1] += 1
        rect[2] -= 1
        rect[3] -= 1
        pygame.draw.rect(self.surface, self.border_color, rect, 1)
        
        # text
        font = utils.fonts[20]
        text_surface = font.render(self.text, True, 'black')
        
        text_width, text_height = text_surface.get_size()
        surface_width, surface_height = self.surface.get_size()
        text_pos = Vector2(surface_width / 2 - text_width / 2, surface_height / 2 - text_height / 2)
        
        self.surface.blit(text_surface, text_pos)
        
        
        screen.blit(self.surface, self.xy)
        
class Label():
    
    def __init__(self, xy, size, text, color):
        self.xy = xy
        self.size = size
        self.text = text
        self.color = pygame.Color(color)
        
        self.surface =  pygame.Surface(size)
        
    def process_event(self, event):
        pass
            
    def update(self):
        pass
                
                
    def draw(self, screen):
        self.surface.fill(self.color)
        
        # border
        rect = self.surface.get_rect()
        pygame.draw.rect(self.surface, game_color, rect, 1)

        # text
        font = utils.fonts[20]
        text_surface = font.render(self.text, True, 'black')
        
        text_width, text_height = text_surface.get_size()
        surface_width, surface_height = self.surface.get_size()
        text_pos = Vector2(surface_width / 2 - text_width / 2, surface_height / 2 - text_height / 2)
        
        self.surface.blit(text_surface, text_pos)
        
        screen.blit(self.surface, self.xy)  
        
        
        



