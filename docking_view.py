#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 18:53:23 2024

@author: steve
"""

import pygame
from pygame.math import Vector2
from enum import Enum

import utils
import constants as const
from game_view import GameView
from gui import Label, Button


INNER_BORDER_WIDTH = 250
INNER_BORDER_HIGHT = 100

class Option(Enum):
    TRADE = 1
    RECRUIT = 2
    BOARD = 3


class BuySell(Enum):
    BUY = 1
    SELL = 2
    

class DockingView(GameView):
    

    
    def __init__(self):
        GameView.__init__(self)   
   
        self.panel = None
        
        button_width = 100
        button_height = 30
        self.top_buttons = {}
 
        y = 150
        x = INNER_BORDER_WIDTH

        self.top_buttons['trade'] = Button((x, y), (button_width, button_height), 'Trade', const.game_color, None, False, self.button_callback)
        x = ( const.screen_width - button_width ) / 2
        self.top_buttons['recruit'] = Button((x, y), (button_width, button_height), 'Recruit', const.game_color, None, False, self.button_callback)
        x = const.screen_width - INNER_BORDER_WIDTH - button_width
        self.top_buttons['board'] = Button((x, y), (button_width, button_height), 'Board', const.game_color, None, False, self.button_callback)
        
        
        
        
    def button_callback(self, button):
        option = Option[button.text.upper()]

        if option == Option.TRADE:
            self.panel = TradePanel(self.current_ship.resources, self.other_ship.resources)
        elif option == Option.RECRUIT:
            self.panel = RecruitPanel()
        elif option == Option.BOARD:
            self.panel = BoardPanel()

        
    def trade_button_callback(self, button):
        pass

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



    
        
class TradePanel():
    
    def __init__(self, our_resources, their_resources):
        
        self.surface = pygame.Surface((const.screen_width, const.screen_height), pygame.SRCALPHA)
        
        button_height = 30
        button_width = 40
        label_width = 100
        spacer = 20

        self.button_map = {}
        self.label_map = {}
        
        self.our_resources = our_resources.copy()
        self.their_resources = their_resources.copy()    
        self.transaction = [0, 0, 0, 0]
   
        resource_width = 70
        buy_x = (const.screen_width - label_width )/2 - spacer - button_width
        label_x = (const.screen_width - label_width )/2
        sell_x = (const.screen_width + label_width )/2 + spacer
        
        offset = 100 - 40
        our_x = offset + INNER_BORDER_WIDTH
        their_x = const.screen_width - offset - resource_width - INNER_BORDER_WIDTH
        
        our_transaction_x = our_x + resource_width + spacer
        their_transaction_x = their_x - spacer - resource_width
        
        y = 200 + INNER_BORDER_HIGHT
        i = 0
        for resource in const.initial_resources.keys():
            if resource != 'credits':
                key = (resource, BuySell.BUY)
                button = Button((buy_x, y), (button_width, button_height), '<', const.game_color, None, False, self.button_callback)
                self.button_map[key] = button
                
                key = (resource, BuySell.SELL)
                button = Button((sell_x, y), (button_width, button_height), '>', const.game_color, None, False, self.button_callback)
                self.button_map[key] = button
                
            
            label_key = (resource.title(), 'Label')
            self.label_map[label_key] = Label((label_x,y), (label_width, button_height), resource.title(), 'gray')
            
            label_key = (resource.title(), 'OurAmount')
            self.label_map[label_key] = Label((our_x,y), (resource_width, button_height), str(self.our_resources[resource]), 'gray')
            label_key = (resource.title(), 'TheirAmount')
            self.label_map[label_key] = Label((their_x,y), (resource_width, button_height), str(self.their_resources[resource]), 'gray')
            
            label_key = (resource.title(), 'OurTxn')
            self.label_map[label_key] = Label((our_transaction_x,y), (resource_width, button_height), str(self.transaction[i]), 'gray')
            label_key = (resource.title(), 'TheirTxn')
            self.label_map[label_key] = Label((their_transaction_x,y), (resource_width, button_height), str(-self.transaction[i]), 'gray')
            
            
            y += button_height + spacer   
            i += 1
    
        self.button_map['Accept'] = Button(((const.screen_width - label_width )/2, y), (label_width, button_height), 'Accept', const.game_color, None, False, self.button_callback)
    

    def process_event(self, event):
             
        for key in self.button_map.keys():
            self.button_map[key].process_event(event)

    def update(self):

        for key in self.button_map.keys():
            self.button_map[key].update()
            
        for key in self.label_map.keys():
            self.label_map[key].update()

            
    def draw(self, screen):
        
        for key in self.button_map.keys():
            self.button_map[key].draw(self.surface)      
            
        for key in self.label_map.keys():
            self.label_map[key].draw(self.surface)
         
    def button_callback(self, button):
        pass
    
    def startup(self, our_resources, their_resources):
        
        i = 0
        #for resource in const.initial_resources.keys():
        #    self.our_resource_amounts[i] = our_resources[resource]
        #    self.their_resource_amounts[i] = their_resources[resource]
        #    i += 1
        
    
    
class RecruitPanel():
    
    def __init__(self):
        
        self.surface = pygame.Surface((const.screen_width, const.screen_height), pygame.SRCALPHA)
    
    def startup(self):
        pass
    
    def process_event(self, event):
        pass

    def update(self):
        pass
    
    def draw(self, screen):
        pass
    

class BoardPanel():
    
    def __init__(self):
        
        self.surface = pygame.Surface((const.screen_width, const.screen_height), pygame.SRCALPHA)

    
    def startup(self):
        pass

    def process_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass



