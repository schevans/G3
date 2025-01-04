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
   
        self.inner_rect = ((INNER_BORDER_WIDTH,INNER_BORDER_HIGHT), (const.screen_width -INNER_BORDER_WIDTH*2, const.screen_height - INNER_BORDER_HIGHT*2) )

        self.option = None
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
        self.option = Option[button.text.upper()]

        if self.option == Option.TRADE:
            self.panel = TradePanel(self.inner_rect[1])
        elif self.option == Option.RECRUIT:
            self.panel = RecruitPanel(self.inner_rect[1])
        elif self.option == Option.BOARD:
            self.panel = BoardPanel(self.inner_rect[1])
            
    def trade_button_callback(self, button):
        pass

    def cleanup(self):
        pass
        
    
    def startup(self, shared_dict):
        self.shared_dict = shared_dict
        self.current_ship = self.shared_dict['current_ship']
        self.other_ship = self.shared_dict['other_ship']
        

        #self.new.startup(self.current_ship.resources, self.other_ship.resources)
        
        
    def process_event(self, event):
             
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                self.next_view = (self.shared_dict['prev_view'], self.shared_dict)
            
        for key in self.top_buttons.keys():
            self.top_buttons[key].process_event(event)
                
    def update(self):
        
        for key in self.top_buttons:
            self.top_buttons[key].update()
                 
    
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
            screen.blit(self.panel.surface,  self.inner_rect[0])



    
        
class TradePanel():
    
    def __init__(self, size):
        
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
        
        button_height = 30
        button_width = 40
        label_width = 100
        spacer = 20

        self.button_map = {}
        self.labels = []
        
        self.our_resource_amounts = [0, 0, 0, 0]
        self.their_resource_amounts = [0, 0, 0, 0]     
        self.transaction = [0, 0, 0, 0]
   
        resource_width = 40
        buy_x = (size[0] - label_width )/2 - spacer - button_width
        label_x = (size[0] - label_width )/2
        sell_x = (size[0] + label_width )/2 + spacer
        
        our_x = 100
        their_x = size[0] - 100 - resource_width
        
        our_transaction_x = our_x + resource_width + spacer
        their_transaction_x = their_x - spacer - resource_width
        
        y = 200
        i = 0
        for resource in const.initial_resources.keys():
            if resource != 'credits':
                key = (resource, BuySell.BUY)
                button = Button((buy_x, y), (button_width, button_height), '<', const.game_color, None, False, self.button_callback)
                self.button_map[key] = button
                
                key = (resource, BuySell.SELL)
                button = Button((sell_x, y), (button_width, button_height), '>', const.game_color, None, False, self.button_callback)
                self.button_map[key] = button
                
            self.labels.append(Label((label_x,y), (label_width, button_height), resource.title(), 'gray'))
            
            self.labels.append(Label((our_x,y), (resource_width, button_height), str(self.our_resource_amounts[i]), 'gray'))
            self.labels.append(Label((their_x,y), (resource_width, button_height), str(self.their_resource_amounts[i]), 'gray'))
            
            self.labels.append(Label((our_transaction_x,y), (resource_width, button_height), str(self.transaction[i]), 'gray'))
            self.labels.append(Label((their_transaction_x,y), (resource_width, button_height), str(-self.transaction[i]), 'gray'))
            
            
            y += button_height + spacer   
            i += 1
    
        self.button_map['Accept'] = Button(((size[0] - label_width )/2, y), (label_width, button_height), 'Accept', const.game_color, None, False, self.button_callback)
    

            

            
    def draw(self, screen):
        
        for key in self.button_map.keys():
            self.button_map[key].draw(self.surface)      
            
        for label in self.labels:             
            label.draw(self.surface)
         
    def button_callback(self, button):
        pass
    
    def startup(self, our_resources, their_resources):
        
        i = 0
        for resource in const.initial_resources.keys():
            self.our_resource_amounts[i] = our_resources[resource]
            self.their_resource_amounts[i] = their_resources[resource]
            i += 1
        
    def update(self):
        
        pass
    
    
class RecruitPanel():
    
    def __init__(self, size):
        
        self.surface = pygame.Surface(size, pygame.SRCALPHA)
    
    def startup(self):
        pass
    
    def draw(self, screen):
        pass
    

class BoardPanel():
    
    def __init__(self, size):
        
        self.surface = pygame.Surface(size, pygame.SRCALPHA)

    
    def startup(self):
        pass


    def draw(self, screen):
        pass



