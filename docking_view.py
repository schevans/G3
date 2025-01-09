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
from gui import Label, Button
from exposition import ExpositionBox, ExpositionText

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

class ButtonType(Enum):
    BUY = 1
    SELL = 2
    ACCEPT = 3
    CANCEL = 4
    
class LabelType(Enum):
    LABEL = 1
    OUR_AMOUNT = 2
    THEIR_AMOUNT = 3
    OUR_TRANSACTION = 4
    THEIR_TRANSACTION = 5
    
    
        
class TradePanel():
    
    def __init__(self, our_ship, their_ship):
        
        self.our_ship = our_ship
        self.their_ship = their_ship
        
        self.surface = pygame.Surface((const.screen_width, const.screen_height), pygame.SRCALPHA)
        
        button_height = 30
        button_width = 40
        label_width = 100
        spacer = 20

        self.button_map = {}
        self.label_map = {}
        
        self.our_resources = our_ship.resources.copy()
        self.their_resources = their_ship.resources.copy()         
        self.transaction = dict.fromkeys(self.our_resources, 0)

        resource_width = 70
        buy_x = (const.screen_width - label_width )/2 - spacer - button_width
        label_x = (const.screen_width - label_width )/2
        sell_x = (const.screen_width + label_width )/2 + spacer
        
        offset = 60
        our_x = offset + INNER_BORDER_WIDTH
        their_x = const.screen_width - offset - resource_width - INNER_BORDER_WIDTH
        
        our_transaction_x = our_x + resource_width + spacer
        their_transaction_x = their_x - spacer - resource_width
        
        y = 200 + INNER_BORDER_HIGHT
        i = 0
        for resource in const.initial_resources.keys():
            if resource != 'credits':
                key = (resource, ButtonType.BUY)
                button = Button((buy_x, y), (button_width, button_height), '<', const.game_color, None, False, self.button_callback)
                self.button_map[key] = button
                
                key = (resource, ButtonType.SELL)
                button = Button((sell_x, y), (button_width, button_height), '>', const.game_color, None, False, self.button_callback)
                self.button_map[key] = button
                
            
            label_key = (resource, LabelType.LABEL)
            self.label_map[label_key] = Label((label_x,y), (label_width, button_height), resource.title(), 'gray')
            
            label_key = (resource, LabelType.OUR_AMOUNT)
            self.label_map[label_key] = Label((our_x,y), (resource_width, button_height), str(self.our_resources[resource]), 'gray')
            label_key = (resource, LabelType.THEIR_AMOUNT)
            self.label_map[label_key] = Label((their_x,y), (resource_width, button_height), str(self.their_resources[resource]), 'gray')
            
            label_key = (resource, LabelType.OUR_TRANSACTION)
            self.label_map[label_key] = Label((our_transaction_x,y), (resource_width, button_height), str(self.transaction[resource]), 'gray')
            label_key = (resource, LabelType.THEIR_TRANSACTION)
            self.label_map[label_key] = Label((their_transaction_x,y), (resource_width, button_height), str(-self.transaction[resource]), 'gray')
            
            y += button_height + spacer   
    
        self.button_map[('Accept', ButtonType.ACCEPT)] = Button((const.screen_width/2 - label_width - spacer/2, y), (label_width, button_height), 'Accept', const.game_color, None, False, self.button_callback)
        
        self.button_map[('Cancel', ButtonType.CANCEL)] = Button((const.screen_width/2 + spacer/2, y), (label_width, button_height), 'Cancel', const.game_color, None, False, self.button_callback)
    
        self.rev_button_map = dict((v, k) for k, v in self.button_map.items())
        self.rev_label_map = dict((v, k) for k, v in self.label_map.items())

    def process_event(self, event):
             
        for key in self.button_map.keys():
            self.button_map[key].process_event(event)


    def update(self):  

        for key in self.button_map.keys():
              
            (resource, button_type) = key 
            button = self.button_map[key]
            button.is_disabled = False
            
            if button_type != ButtonType.ACCEPT and button_type != ButtonType.CANCEL:
                            
                if self.our_resources['credits'] < 1:
                    if button_type == ButtonType.BUY:
                        button.is_disabled = True
                        
                if self.their_resources['credits'] < 1:
                    if button_type == ButtonType.SELL:
                        button.is_disabled = True                    
                
                if self.our_resources[resource] < 1 and button_type == ButtonType.SELL:
                    button.is_disabled = True 
                    
                if self.their_resources[resource] < 1 and button_type == ButtonType.BUY:
                    button.is_disabled = True 
                    
            button.update()
            
            
        for key in self.label_map.keys():
            
            # FIXME: Something wrong here..
            if key != 'Accept':
                (resource, label_type) =  key
                   
                self.label_map[(resource, LabelType.OUR_TRANSACTION)].text = str(self.transaction[resource])
                self.label_map[(resource, LabelType.THEIR_TRANSACTION)].text = str(-self.transaction[resource])
                self.label_map[(resource, LabelType.OUR_AMOUNT)].text = str(self.our_resources[resource])
                self.label_map[(resource, LabelType.THEIR_AMOUNT)].text = str(self.their_resources[resource])
                
                
    def draw(self, screen):
        
        for key in self.button_map.keys():
            self.button_map[key].draw(self.surface)      
            
        for key in self.label_map.keys():
            self.label_map[key].draw(self.surface)
         
    def button_callback(self, button):
        (resource, button_type) = self.rev_button_map[button]
                    
        if button_type == ButtonType.ACCEPT:
            self.our_ship.resources = self.our_resources
            self.their_ship.resources = self.their_resources
            self.transaction = dict.fromkeys(self.transaction, 0)
        elif button_type == ButtonType.CANCEL:
            self.our_resources = self.our_ship.resources.copy()
            self.their_resources = self.their_ship.resources.copy()
            self.transaction = dict.fromkeys(self.transaction, 0)
        else:
            buysell = 1 if button_type == ButtonType.BUY else -1
            amount = const.fx_rates[self.their_ship.liege][resource] * buysell
            
            self.transaction[resource] += buysell
            self.our_resources[resource] += buysell
            self.their_resources[resource] -= buysell
            
            self.transaction['credits'] -= amount
            self.our_resources['credits'] -= amount
            self.their_resources['credits'] += amount
    
    
class ApproachPanel():
    
    def __init__(self, their_ship):
        self.their_ship = their_ship
        
        self.surface = pygame.Surface((const.screen_width, const.screen_height), pygame.SRCALPHA)
        
        text = 'Approach ' + self.their_ship.description()       
        text_width = utils.fonts[20].size(text)[0]
        button_width = text_width + 60
        button_height = 50
        button_x = (const.screen_width - button_width) / 2
        button_y = 200 + INNER_BORDER_HIGHT
        
        self.button = Button((button_x, button_y), (button_width, button_height), text, const.game_color, None, False, self.callback)


    def callback(self, button):
        self.their_ship.approach()
        self.button.is_disabled = True
        
    def process_event(self, event):
        self.button.process_event(event)

    def update(self):
        self.button.update()
    
    def draw(self, screen):
        self.button.draw(self.surface)
    

class BoardPanel():
    
    def __init__(self):
        
        self.surface = pygame.Surface((const.screen_width, const.screen_height), pygame.SRCALPHA)


    def process_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass



