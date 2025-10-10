#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 18:53:23 2024

@author: steve
"""

from pygame.math import Vector2
import json

import utils
import constants as const
from game_view import GameView, View
from gui import Label, Button

got_color = 'mediumseagreen'
available_color = 'grey'
unavilable_color = 'gray56'

with open('./data/ship_system_descriptions.json') as f:
     system_descriptions = json.load(f)

class FittingView(GameView):
    
    def __init__(self):
        GameView.__init__(self)   
        
        self.button_map = {}
        self.rev_button_map = {}
        self.labels = []
        
        label_width = 130
        button_width = 80
        space = 20
        
        width = label_width + (space+button_width) * 4
        height = (len(self.current_ship.fit.system_names) * 40) - 10
        
        pos = Vector2(const.screen_width / 2 - width / 2, const.screen_height / 2 - height / 2)
        
        x = pos[0]
        y = pos[1]
        for key in self.current_ship.fit.system_names:   
            x = pos[0]
            mouseover_text = system_descriptions.get(key, [['#MISSING# from data/system_descriptions.json']])
            self.labels.append(Label((x,y), (label_width, 30), key.title(), 'gray', mouseover_text))
            
            x += label_width+space
            current_level = self.current_ship.fit.level(key)
            level = 0
            while level <= 3:
                
                function = key.title() + ': ' + str(self.current_ship.fit.systems[key].data[str(level)])
                upgrade_cost = self.current_ship.fit.systems[key].get_upgrade_cost_str(level)  
                
                is_disabled = True
                mousover_text = [function]
                if level <= current_level:
                    color = got_color                  
                elif level == current_level + 1:
                    color = available_color
                    is_disabled = False
                    mousover_text += upgrade_cost
                else:
                    color = unavilable_color
                    mousover_text += upgrade_cost
                    
                button = Button((x, y), (button_width, 30), utils.numbers_to_roman(level), color, mousover_text, is_disabled, self.button_callback)
                self.button_map[button] = (key, level)
                self.rev_button_map[(key, level)] = button
                
                level += 1
                x += button_width+space
            y += 40
        
            
    def cleanup(self):
        pass
        
    def startup(self, shared_dict):
        self.shared_dict = shared_dict
        self.shared_dict['history'].append(View.FITTING)
        self.current_ship = self.shared_dict['current_ship']
        
    def process_event(self, event):

        GameView.process_event(self, event)   

        for widget in list(self.button_map.keys()) + self.labels:
            widget.process_event(event)
            
        
    def update(self):
        
        # FIXME: Dup with init
        for button in self.button_map.keys():
            key, level = self.button_map[button]
            current_level = self.current_ship.fit.level(key)
            
            function = key.title() + ': ' + str(self.current_ship.fit.systems[key].data[str(level)])
            upgrade_cost = self.current_ship.fit.systems[key].get_upgrade_cost_str(level)  
            
            button.is_disabled = True
            button.mouseover_text = [function]
            color = unavilable_color
            if level <= current_level:
                color = got_color                  
            elif level == current_level + 1:
                if self.current_ship.can_upgrade(key):
                    color = available_color
                    button.is_disabled = False
                button.mouseover_text += upgrade_cost
            else:
                button.mouseover_text += upgrade_cost
                
            button.set_color(color)

        for button in self.button_map.keys():
            button.update()       
                 
    
    def draw_background(self, screen):
        GameView.draw(self, screen)
                
        ship_image = utils.scale_and_monochrome_ship_image(self.current_ship)
        
        width, height = ship_image.get_size()
        
        screen.blit(ship_image, (const.screen_width/2 - width/2, const.screen_height/2 - height/2 + 60))        

        # ship name
        ship_name = self.current_ship.get_long_name()
        text_y = const.screen_height - 50
        text_surface = utils.fonts[20].render(ship_name, True, 'white')    
        text_width = utils.fonts[20].size(ship_name)[0]
        text_x = const.screen_width/2 - text_width/2
        screen.blit(text_surface, (text_x, text_y))
            
    
    def draw(self, screen):

        self.draw_background(screen)
        
        for button in self.button_map.keys():
            button.draw(screen)  

        for label in self.labels:             
            label.draw(screen)
            
        # mouseover text - need to do this after all the buttons/labels have rendered
        for widget in list(self.button_map.keys()) + self.labels:
            if widget.is_active:
                self.draw_mouseover_text(screen, widget.mouseover_text)       

        
    def button_callback(self, button):
        
        system, level = self.button_map[button]
        
        if self.current_ship.can_upgrade(system):
            
            self.current_ship.upgrade_system(system)
            
            button.is_disabled = True
            button.set_color(got_color)
            button.mouseover_text = [button.mouseover_text[0]]
            
            if level < 3:
                next_button = self.rev_button_map[(system,level+1)]
                next_button.is_disabled = False
                next_button.set_color(available_color)



