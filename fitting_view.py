#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 18:53:23 2024

@author: steve
"""

import pygame
from pygame.math import Vector2
import collections

import utils
import constants as const
from game_view import GameView

game_color = (255, 181, 108)

class Button():
    
    def __init__(self, xy, size, text, color):
        self.xy = xy
        self.size = size
        self.text = text
        self.color = pygame.Color(color)
        
        self.lighter_color = utils.whiten_a_bit(self.color, 0.5)
        self.darker_color = utils.fade_to_black(self.color, 1, 2)
        self.border_color = self.lighter_color
        self.button_color = self.color
        
        self.surface =  pygame.Surface(size)

        
    def process_event(self, event):
        is_active = False
        mousepos = pygame.mouse.get_pos()
        if pygame.Rect(self.xy, self.size).collidepoint(mousepos):
            self.button_color = self.lighter_color
            is_active = True
        else:
            self.button_color = self.color
              
        leftclick, _, _ = pygame.mouse.get_pressed()

        if leftclick and is_active:
            self.button_color = self.darker_color
            self.border_color = 'black'
    
    def update(self):
        pass


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
        
    def set_color(self, color):
        self.color = pygame.Color(color)

class FittingView(GameView):
    
    def __init__(self):
        GameView.__init__(self)   
        
        self.old_view = None
        
        self.buttons = collections.defaultdict(dict)
        
        
        label_width = 120
        button_width = 80
        space = 20
        
        x_spacing = [0, label_width+space, space+button_width,  space+button_width,   space+button_width]
        
        width = sum(x_spacing) + button_width
        height = (len(self.current_ship.fit.fit_level.keys()) * 40) - 10
        
        pos = Vector2(const.screen_width / 2 - width / 2, const.screen_height / 2 - height / 2)
        
        x = pos[0]
        col = 0
        while col <= 4:
            x += x_spacing[col]
            y_offset = pos[1]
            if col == 0:
                for key in self.current_ship.fit.fit_level.keys():
                    self.buttons[col][key] = Button((x,y_offset), (label_width, 30), key, 'gray')
                    y_offset += 40
            else:
                for key in self.current_ship.fit.fit_level.keys():                    
                    self.buttons[col][key] = Button((x, y_offset), (button_width, 30), utils.numbers_to_roman(col), 'gray')
                    y_offset += 40
            col += 1
            
            

        
        
        
    def cleanup(self):
        pass
        
    def startup(self, view):  
        self.old_view = view
    
    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                self.next_view = self.old_view
             
        for col in self.buttons:
            for system in self.buttons[col]:                    
                self.buttons[col][system].process_event(event)
                    
    def update(self):

              

        for system in self.current_ship.fit.fit_level.keys():
            level = int(self.current_ship.fit.fit_level[system])
            for backfill in range(0, level+1):
                self.buttons[backfill+1][system].set_color('darkgreen')
                

            
        for col in self.buttons:
            for system in self.buttons[col]:            
                self.buttons[col][system].update()
    
    def draw_background(self, screen):
        GameView.draw(self, screen)
        
        ship_image = self.current_ship.image_still.original_image.copy()
        
        width, height = ship_image.get_size()
        for x in range(width):
            for y in range(height):
                
                red, green, blue, alpha = ship_image.get_at((x, y))
                
                if red < 10 and green < 10 and blue < 10:
                    ship_image.set_at((x, y), pygame.Color(0, 0, 0, alpha))
                else:
                    ship_image.set_at((x, y), pygame.Color(25, 25, 25, alpha))
                
                
        ship_image = pygame.transform.scale_by(ship_image, const.screen_height/height)
        
        width, height = ship_image.get_size()
        
        screen.blit(ship_image, (const.screen_width/2 - width/2, const.screen_height/2 - height/2 + 60))        
    
    def draw(self, screen):

        self.draw_background(screen)
        
        for col in self.buttons:
            for system in self.buttons[col]:            
                self.buttons[col][system].draw(screen)
        


        






