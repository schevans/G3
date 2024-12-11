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
 
LEFT_MOUSE_CLICK = 1       
EXPOSITION_BOX_SIZE = 100
       
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
        
        if not self.is_disabled and self.is_active:
            self.is_pressed = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_CLICK:
            #if event.type == pygame.KEYDOWN and pygame.K_RETURN:
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
        
        self.lighter_color = utils.whiten_a_bit(self.color, 0.5)
        self.darker_color = utils.fade_to_black(self.color, 1, 2)
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
        

class ExpostionBox():
    
    def __init__(self, text, callback):
        self.text = text
        
        self.surface = pygame.Surface((const.screen_width, const.screen_height), pygame.SRCALPHA)

        # FIXME: Note 30 is is the same as in button above. Abstracify        
        button_pos = Vector2(const.screen_width / 2 - 100 / 2, const.screen_height - EXPOSITION_BOX_SIZE - 30 - 30)
        self.button = Button(button_pos, (100,30), 'OK', const.game_color, None, False, callback)
        
    def process_event(self, event):
        
        self.button.process_event(event)
        
    def update(self):
        self.button.update()
    
    def draw(self, screen):   

        # inner text box
        inner_rect = pygame.Rect(EXPOSITION_BOX_SIZE, EXPOSITION_BOX_SIZE, const.screen_width - 2*EXPOSITION_BOX_SIZE, const.screen_height - 2*EXPOSITION_BOX_SIZE)
        pygame.draw.rect(self.surface, pygame.Color(0,0,0,255), inner_rect) 
    
        # border
        border = 10
        pygame.draw.rect(self.surface, const.game_color, inner_rect, 1)
        inner_rect[0] += border
        inner_rect[1] += border
        inner_rect[2] -= border*2
        inner_rect[3] -= border*2
        pygame.draw.rect(self.surface, const.game_color, inner_rect, 1)

        # text
        font = utils.fonts[20]
        text_surface = font.render(self.text[1], True, 'white')     
        text_width, text_height = text_surface.get_size()
        surface_width, surface_height = self.surface.get_size()
        text_pos = Vector2(surface_width / 2 - text_width / 2, surface_height / 2 - text_height / 2)
        self.surface.blit(text_surface, text_pos )
        
        # button
        self.button.draw(self.surface)
         
        screen.blit(self.surface,(0,0))

