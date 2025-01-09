#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 18:53:23 2024

@author: steve
"""

import pygame
from enum import Enum

import utils
import constants as const
from game_view import GameView
from gui import Button
from docking_panels import TradePanel, ApproachPanel, BoardPanel

INNER_BORDER_WIDTH = 250
INNER_BORDER_HIGHT = 100

class Panel(Enum):
    TRADE = 1
    APPROACH = 2
    BOARD = 3

class DockingView(GameView):
    

    
    def __init__(self):
        GameView.__init__(self)   
   
        self.panel = None
        
        button_width = 120
        button_height = 30
        
        # FIXME: Not needed I think - array. Button text used in button_callback instead of rev_top_buttons
        self.top_buttons = {}
 
        y = 150
        x = INNER_BORDER_WIDTH

        self.top_buttons[Panel.TRADE] = Button((x, y), (button_width, button_height), 'Trade', const.game_color, None, False, self.button_callback)
        x = ( const.screen_width - button_width ) / 2
        self.top_buttons[Panel.APPROACH] = Button((x, y), (button_width, button_height), 'Approach', const.game_color, None, False, self.button_callback)
        x = const.screen_width - INNER_BORDER_WIDTH - button_width
        self.top_buttons[Panel.BOARD] = Button((x, y), (button_width, button_height), 'Board', const.game_color, None, False, self.button_callback)
        
        
        
        
    def button_callback(self, button):
        panel = Panel[button.text.upper()]

        if panel == Panel.TRADE:
            self.panel = TradePanel(self.current_ship, self.other_ship)
        elif panel == Panel.APPROACH:
            self.panel = ApproachPanel(self.other_ship)
        elif panel == Panel.BOARD:
            self.panel = BoardPanel()
            


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
            
        for key in self.top_buttons.keys():
            self.top_buttons[key].process_event(event)
            
        if self.panel:
            self.panel.process_event(event)
                
    def update(self):
        
        for key in self.top_buttons:
            self.top_buttons[key].update()
           
        if self.panel:
            self.panel.update()
        
        
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
        
        for key in self.top_buttons:
            self.top_buttons[key].draw(screen)
            
        if self.panel:
            self.panel.draw(screen)
            screen.blit(self.panel.surface,  (0,0))







