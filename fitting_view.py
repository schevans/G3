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
from gui import Label, Button

class FittingView(GameView):
    
    def __init__(self):
        GameView.__init__(self)   
        
        self.old_view = None
        
        self.buttons = collections.defaultdict(dict)
        self.labels = []
        
        label_width = 120
        button_width = 80
        space = 20
        
        x_spacing = [0, label_width+space, space+button_width,  space+button_width,   space+button_width]
        
        width = sum(x_spacing) + button_width
        height = (len(self.current_ship.fit.system_names) * 40) - 10
        
        pos = Vector2(const.screen_width / 2 - width / 2, const.screen_height / 2 - height / 2)
        
        x = pos[0]
        y_offset = pos[1]
        for key in self.current_ship.fit.system_names:             
            self.labels.append(Label((x,y_offset), (label_width, 30), key.title(), 'gray'))
            y_offset += 40
        
        col = 0
        x += label_width+space
        while col <= 3:
            y_offset = pos[1]
            for key in self.current_ship.fit.system_names:             
                mousover_text = self.current_ship.fit.systems[key].get_upgrade_cost(col)  
                self.buttons[col][key] = Button((x, y_offset), (button_width, 30), utils.numbers_to_roman(col+1), 'gray', mousover_text)
                y_offset += 40            
            col += 1
            x += space+button_width
            

        
        
        
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

              

        for system in self.current_ship.fit.system_names:
            level = int(self.current_ship.fit.systems[system].level)
            for backfill in range(0, level+1):
                self.buttons[backfill][system].is_disabled = True
                

        button_pressed = None   
        for col in self.buttons:
            for system in self.buttons[col]:            
                self.buttons[col][system].update()
                
                if self.buttons[col][system].is_pressed:
                    button_pressed = self.buttons[col][system]
                    
        if button_pressed:
            print(button_pressed.text)
    
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
        
        for col in self.buttons:
            for system in self.buttons[col]:  
                if self.buttons[col][system].is_active:
                    self.draw_mouseover_text(screen, pygame.mouse.get_pos(), self.buttons[col][system].mouseover_text)
        
        for label in self.labels:             
            label.draw(screen)

        






