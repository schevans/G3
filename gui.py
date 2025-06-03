#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 18:43:09 2024

@author: steve
"""

import pygame
from pygame import Vector2

import utils
import constants as const
  
       
class Button():
    
    def __init__(self, xy, size, text, color, mouseover_text, is_disabled, callback):
        self.xy = xy
        self.size = size
        self.text = text
        self.set_color(pygame.Color(color))
        self.mouseover_text = mouseover_text
        self.is_disabled = is_disabled
        self.callback = callback
        
        self.is_active = False
        self.is_pressed = False
        self.font = utils.fonts[20]
        self.surface =  pygame.Surface(size)

  
    def process_event(self, event):
    
        mousepos = pygame.mouse.get_pos()
        if pygame.Rect(self.xy, self.size).collidepoint(mousepos):
            self.button_color = self.lighter_color
            self.is_active = True
        else:
            self.button_color = self.color
            self.is_active = False
        
        self.is_pressed = False
        if not self.is_disabled and self.is_active:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == const.left_mouse_click:
            #if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                self.is_pressed = True
                self.callback(self)

    def update(self):
        
        if self.is_pressed or self.is_disabled:
            self.button_color = self.darker_color
            self.border_color = 'black'
        elif self.is_active:
            self.button_color = self.lighter_color
        else:
            self.border_color = self.lighter_color
            self.button_color = self.color


    def draw(self, screen):

        self.surface.fill(self.button_color)
        
        # border
        rect = self.surface.get_rect()
        pygame.draw.rect(self.surface, const.game_color, rect, 1)
        rect[0] += 1
        rect[1] += 1
        rect[2] -= 1
        rect[3] -= 1
        pygame.draw.rect(self.surface, const.game_color, rect, 1)
        
        # label
        text_surface = self.font.render(self.text, True, 'black')
        
        text_width, text_height = text_surface.get_size()
        surface_width, surface_height = self.surface.get_size()
        text_pos = Vector2(surface_width / 2 - text_width / 2, surface_height / 2 - text_height / 2)
        
        self.surface.blit(text_surface, text_pos)
        
        screen.blit(self.surface, self.xy)
        
    
    def set_color(self, color):
        self.color = pygame.Color(color)
        
        self.lighter_color = utils.fade_color_to(self.color, pygame.Color('white'), 0.5)
        self.darker_color = utils.fade_color_to(self.color, pygame.Color('black'), 1/2)
        self.border_color = self.lighter_color
        self.button_color = self.color
        
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
        pygame.draw.rect(self.surface, const.game_color, rect, 1)

        # text
        font = utils.fonts[20]
        text_surface = font.render(self.text, True, 'black')
        
        text_width, text_height = text_surface.get_size()
        surface_width, surface_height = self.surface.get_size()
        text_pos = Vector2(surface_width / 2 - text_width / 2, surface_height / 2 - text_height / 2)
        
        self.surface.blit(text_surface, text_pos)
        
        screen.blit(self.surface, self.xy)  
        

class CheckBox():
    
    def __init__(self, xy, size, text, color, is_checked, callback):
        self.xy = xy
        self.size = size
        self.text = text
        self.color = pygame.Color(color)
        self.is_checked = is_checked
        self.callback = callback
        
        self.spacer = 5
        self.background_color = pygame.Color('black')
        self.lighter_color =  utils.fade_color_to(self.color, pygame.Color('black'), 2/3)
        self.is_pressed = False
        
        self.text_surface = utils.fonts[14].render(text, True, 'white')
        text_width, text_height = self.text_surface.get_size()
        
        self.surface =  pygame.Surface((size[0] + text_width + self.spacer, max(size[1], text_height) ))
  
  
    def process_event(self, event):
        
        mousepos = pygame.mouse.get_pos()
        if pygame.Rect(self.xy, self.size).collidepoint(mousepos):
            self.background_color = self.lighter_color
            self.is_active = True
        else:
            self.background_color = pygame.Color('black')
            self.is_active = False
            
        if self.is_active:
            self.is_pressed = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_CLICK:
            #if event.type == pygame.KEYDOWN and pygame.K_RETURN:
                self.is_checked = not self.is_checked
                self.callback(self.is_checked)
            
            
    def update(self):
        pass

    def draw(self, screen):

        self.surface.fill('black')

        pygame.draw.rect(self.surface, self.background_color, ((0,0), self.size))

        pygame.draw.rect(self.surface, self.color, ((0,0), self.size), 2)

        if self.is_checked:
            pygame.draw.line(self.surface, self.color, (0,0), self.size, 1)
            pygame.draw.line(self.surface, self.color, (self.size[0], 0), (0, self.size[1]), 1)
            
        self.surface.blit(self.text_surface, (self.size[0] + self.spacer , 1))
        
        screen.blit(self.surface, self.xy)
        
    







