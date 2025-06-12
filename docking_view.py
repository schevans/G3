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
from game_view import GameView, View
from gui import Button
from docking_panels import TradePanel, ApproachPanel, BoardPanel, RepairPanel, INNER_BORDER_WIDTH
from exposition import ExpositionBox, ExpositionText


class Panel(Enum):
    TRADE = 1
    APPROACH = 2
    BOARD = 3,
    REPAIR = 4

class DockingView(GameView):
    

    
    def __init__(self):
        GameView.__init__(self)   
   
        self.panel = None
        
        self.button_width = 120
        self.button_height = 30
        
        # FIXME: Not needed I think - array. Button text used in button_callback instead of rev_top_buttons
        self.top_buttons = {}
 

        
    def approach_callback(self, button):
        
        expo_enum = ExpositionText.NO
        if self.other_ship.liege == const.friendly_capital:
            expo_enum = ExpositionText.YES
            self.other_ship.recruit() 
        elif self.other_ship.liege == const.neutral_capital:
            expo_enum = ExpositionText.NO_THANKS
        
        button.is_disabled = True
        self.exposition = ExpositionBox(expo_enum, self.exposition_ok_callback, self.exposition_ok_callback, False)
        
    def repair_callback(self, button):
        pass
        
    def button_callback(self, button):
        panel = Panel[button.text.upper()]

        if panel == Panel.TRADE:
            self.panel = TradePanel(self.current_ship, self.other_ship)
        elif panel == Panel.APPROACH:
            self.panel = ApproachPanel(self.other_ship, self.approach_callback)
        elif panel == Panel.BOARD:
            self.panel = BoardPanel()
        elif panel == Panel.REPAIR:
            self.panel = RepairPanel(self.current_ship, self.repair_callback)
            
       
    def cleanup(self):
        self.panel = None
        self.top_buttons.clear()
        
    
    def startup(self, shared_dict):
        self.shared_dict = shared_dict
        self.shared_dict['history'].append(View.DOCKING)
        self.current_ship = self.shared_dict['current_ship']
        self.other_ship = self.shared_dict['other_ship']
        
        y = 150
        x = INNER_BORDER_WIDTH

        self.top_buttons[Panel.TRADE] = Button((x, y), (self.button_width, self.button_height), 'Trade', const.game_color, None, False, self.button_callback)
        
        if self.other_ship.object_type() == 'Ship':
            x = ( const.screen_width - self.button_width ) / 2
            self.top_buttons[Panel.APPROACH] = Button((x, y), (self.button_width, self.button_height), 'Approach', const.game_color, None, False, self.button_callback)
            x = const.screen_width - INNER_BORDER_WIDTH - self.button_width
            self.top_buttons[Panel.BOARD] = Button((x, y), (self.button_width, self.button_height), 'Board', const.game_color, None, False, self.button_callback)
        else: # station
            x = const.screen_width - INNER_BORDER_WIDTH - self.button_width
            self.top_buttons[Panel.REPAIR] = Button((x, y), (self.button_width, self.button_height), 'Repair', const.game_color, None, False, self.button_callback)
            

        
    def process_event(self, event):
             
        GameView.process_event(self, event)
            
        for key in self.top_buttons.keys():
            self.top_buttons[key].process_event(event)
            
        if self.panel:
            self.panel.process_event(event)
                
    def update(self):
        
        GameView.update(self)
        
        for key in self.top_buttons:
            self.top_buttons[key].update()
           
        if self.panel:
            self.panel.update()
        
        
    def draw_background(self, screen):
        GameView.draw(self, screen)
        
        other_ship_image = utils.scale_and_monochrome_ship_image(self.other_ship)
    
        if self.other_ship.object_type() == 'Ship':
            
            current_ship_image = utils.scale_and_monochrome_ship_image(self.current_ship)

            width, height = current_ship_image.get_size()
            screen.blit(current_ship_image, (30, const.screen_height/2 - height/2 + 60))            
            
            width, height = other_ship_image.get_size()
            
            screen.blit(other_ship_image, (const.screen_width - width, const.screen_height/2 - height/2 + 60))    
            
            faded_gray = (25, 25, 25)   # FIXME: DUP in utils.scale_and_monochrome_ship_image
            rect = ((30+width, (3*const.screen_height/5) - 60), (const.screen_width - width*2 + 60, 60))
                 
            pygame.draw.rect(screen, faded_gray, rect)

            text_y = const.screen_height - 50
            text_surface = self.font.render(self.current_ship.description(), True, 'white')    
            text_width = self.font.size(self.current_ship.description())[0]
            text_x = 30 + width/2 - text_width/2
            screen.blit(text_surface, (text_x, text_y))
            
            text_surface = self.font.render(self.other_ship.description(), True, 'white')    
            text_width = self.font.size(self.other_ship.description())[0]
            text_x = const.screen_width - width/2 - text_width/2
            screen.blit(text_surface, (text_x, text_y))
            
        else:  # is station
            
            width, height = other_ship_image.get_size()
            screen.blit(other_ship_image, (const.screen_width - width, const.screen_height/2 - height/2 + 60))    
            
            text_y = const.screen_height - 50
            text_surface = self.font.render(self.other_ship.description(), True, 'white')   
            text_width = self.font.size(self.other_ship.description())[0]
            text_x = const.screen_width/2 - text_width/2
            screen.blit(text_surface, (text_x, text_y))

            
    def draw(self, screen):

        self.draw_background(screen)
        
        for key in self.top_buttons:
            self.top_buttons[key].draw(screen)
            
        if self.panel:
            self.panel.draw(screen)
            screen.blit(self.panel.surface,  (0,0))

        GameView.draw_objects(self, screen) 







