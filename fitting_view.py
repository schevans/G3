#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 18:53:23 2024

@author: steve
"""

from pygame.math import Vector2

import utils
import constants as const
from game_view import GameView, View
from gui import Label, Button

got_color = 'green4'
available_color = 'grey'
unavilable_color = 'gray39'

class FittingView(GameView):
    

    
    def __init__(self):
        GameView.__init__(self)   
        
        self.button_map = {}
        self.rev_button_map = {}
        self.labels = []
        
        label_width = 120
        button_width = 80
        space = 20
        
        width = label_width + (space+button_width) * 4
        height = (len(self.current_ship.fit.system_names) * 40) - 10
        
        pos = Vector2(const.screen_width / 2 - width / 2, const.screen_height / 2 - height / 2)
        
        x = pos[0]
        y = pos[1]
        for key in self.current_ship.fit.system_names:   
            x = pos[0]
            self.labels.append(Label((x,y), (label_width, 30), key.title(), 'gray'))
            
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

        for button in self.button_map.keys():
            button.process_event(event)
            
        
    def update(self):
        
        # TODO PROFILE: Allways called. 
        # FIXME: Dup with init
        for button in self.button_map.keys():
            key, level = self.button_map[button]
            current_level = self.current_ship.fit.level(key)
            
            function = key.title() + ': ' + str(self.current_ship.fit.systems[key].data[str(level)])
            upgrade_cost = self.current_ship.fit.systems[key].get_upgrade_cost_str(level)  
            
            button.is_disabled = True
            button.mousover_text = [function]
            color = unavilable_color
            if level <= current_level:
                color = got_color                  
            elif level == current_level + 1:
                color = available_color
                button.is_disabled = False
                button.mousover_text += upgrade_cost
            else:
                button.mousover_text += upgrade_cost   
                
            button.set_color(color)
            

        for button in self.button_map.keys():
            button.update()       
                 
    
    def draw_background(self, screen):
        GameView.draw(self, screen)
                
        ship_image = utils.scale_and_monochrome_ship_image(self.current_ship)
        
        width, height = ship_image.get_size()
        
        screen.blit(ship_image, (const.screen_width/2 - width/2, const.screen_height/2 - height/2 + 60))        
    
    def draw(self, screen):

        self.draw_background(screen)
        
        for button in self.button_map.keys():
            button.draw(screen)  

        # mouseover text - need to do this after all the buttons have rendered
        for button in self.button_map.keys():
            if button.is_active:
                self.draw_mouseover_text(screen, button.mouseover_text)

        for label in self.labels:             
            label.draw(screen)

        
    def button_callback(self, button):
        
        system, level = self.button_map[button]
        
        self.current_ship.upgrade_system(system)
        
        button.is_disabled = True
        button.set_color(got_color)
        button.mouseover_text = [button.mouseover_text[0]]
        
        if level < 3:
            next_button = self.rev_button_map[(system,level+1)]
            next_button.is_disabled = False
            next_button.set_color(available_color)



