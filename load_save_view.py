#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  3 18:45:27 2025

@author: steve
"""

from pygame import Vector2
from game_view import GameView, View
import glob
import os

import constants as const
from gui import Label, Button
import utils

available_color = 'grey'

data_dir = './data/'

class LoadSaveView(GameView):

    def __init__(self):
        GameView.__init__(self) 
        
        self.save_spot_rows = 10
        self.save_spot_cols = 2
        
        self.save_slot_buttons = []
        self.save_slot_lables = []
        
        self.file_name = None 
        self.is_load_view = True
        
        label_width = 300
        button_width = 150
        file_button_width = 80
        space = 20
        
        files_width = (label_width + file_button_width + space) * self.save_spot_cols + space * 2
        files_height = (self.save_spot_rows * 40) - 10
        
        files_pos = Vector2(const.screen_width / 2 - files_width / 2, const.screen_height / 2 - files_height / 2)
        
        
        self.load_select_button = Button((const.screen_width/2-button_width-space, 100), (button_width, 30), 'Load Menu', const.game_color, None, False, self.button_callback)
        self.save_select_button = Button((const.screen_width/2+space, 100), (button_width, 30), 'Save Menu', available_color, None, False, self.button_callback)
        self.load_save_button = Button((const.screen_width/2-button_width/2, 700), (button_width, 30), 'Load', const.game_color, None, True, self.button_callback)
        
        legend ='Key: RtP SaveNum RandomSeed DaysPassed NumAllies CurrentShip'
        self.legend_surface = utils.fonts[20].render(legend, True, 'white')
        legend_width, legend_height = self.legend_surface.get_size()
        self.legend_xy = Vector2(const.screen_width / 2 - legend_width / 2, 150)

        overwrite_text = 'Warning: Overwriting save file'
        self.overwrite_surface = utils.fonts[20].render(overwrite_text, True, 'white')
        overwrite_width, overwrite_height = self.overwrite_surface.get_size()
        self.overwrite_xy = Vector2(const.screen_width / 2 - overwrite_width / 2, 640)
        self.overwrite_file = None

        x = files_pos[0]
        y = files_pos[1]
        
        i = 1
        for c in range(self.save_spot_cols):
        
            for r in range(self.save_spot_rows):

                self.save_slot_buttons.append(Button((x, y), (file_button_width, 30), str(i), available_color, None, False, self.button_callback))
                
                self.save_slot_lables.append(Label((x+file_button_width+space,y), (label_width, 30), None, 'gray45'))
                
                y += 40
                i += 1
            x += file_button_width + label_width + space * 3
            y = files_pos[1]
        
        
        self.load_file_slots()

        self.widgets = [self.load_select_button, self.save_select_button, self.load_save_button] + self.save_slot_buttons + self.save_slot_lables
        
        
    def load_file_slots(self):
        
        files = glob.glob(data_dir + 'RtP_*.pkl')
        
        for label in self.save_slot_lables:
            label.text = None
        
        for file in files:
            save_slot_number = int(file.split('_')[1]) - 1
            label_text = os.path.basename(file).split('.')[0]
            self.save_slot_lables[save_slot_number].text = label_text

    def reset_slots(self):

        self.file_name = None
        self.load_save_button.is_disabled = True
        self.overwrite_file = None
        
        for button in self.save_slot_buttons:
            button.set_color(available_color)    
            
        for label in self.save_slot_lables:
            label.text = None

        self.load_file_slots()
        
        
    def cleanup(self):        
        self.is_load_view = True
        self.load_save_button.text = 'Load'
        self.reset_slots()
        
        
    def startup(self, shared_dict):
        self.shared_dict = shared_dict
        self.shared_dict['history'].append(View.LOAD_SAVE)
        self.current_ship = self.shared_dict['current_ship']
        self.master_timer = self.shared_dict['master_timer']
        
        self.load_file_slots()
        
    def process_event(self, event):

        GameView.process_event(self, event)   
        
        for widget in self.widgets:
            widget.process_event(event)
            
            
    def update(self):

        self.load_select_button.set_color(const.game_color if self.is_load_view else available_color)
        self.save_select_button.set_color(available_color if self.is_load_view else const.game_color)        

        for widget in self.widgets:
            widget.update()  
                     
        for i in range(len(self.save_slot_buttons)):
            if self.is_load_view:
                if not self.save_slot_lables[i].text:
                    self.save_slot_buttons[i].is_disabled = True
            else:
                self.save_slot_buttons[i].is_disabled = False
                    

    def draw(self, screen):
        
        GameView.draw(self, screen)
        
        for widget in self.widgets:
            widget.draw(screen)  

        screen.blit(self.legend_surface, self.legend_xy)

        if self.overwrite_file:        
            screen.blit(self.overwrite_surface, self.overwrite_xy)
        
        
    def button_callback(self, button):
        
        if button == self.load_select_button:
            self.is_load_view = True
            self.load_save_button.text = 'Load'
            self.reset_slots()   
            
        elif button == self.save_select_button:
            self.is_load_view = False
            self.load_save_button.text = 'Save'
            self.reset_slots()   
            
        elif button in self.save_slot_buttons:
            
            self.reset_slots()          
            button.set_color(const.game_color)
            index = self.save_slot_buttons.index(button)
            self.load_save_button.is_disabled = False
            self.overwrite_file = None
            
            if self.is_load_view:
                self.file_name = self.save_slot_lables[index].text 
            else:                  
                num_alies = sum(x.is_npc == False and x.is_alive for x in self.ships) - 1
                self.file_name = 'RtP_' + self.save_slot_buttons[index].text + '_' + str(const.random_seed) + '_' + str(self.master_timer()) + '_' + str(num_alies) + '_' + self.current_ship.name
                
                if self.save_slot_lables[index].text:
                    self.overwrite_file = self.save_slot_lables[index].text
                    
                self.save_slot_lables[index].text = self.file_name
                
        elif button == self.load_save_button:
            
            if self.file_name:
                
                if self.overwrite_file:
                    full_path = data_dir + self.overwrite_file + '.pkl'
                    os.remove(full_path)
                    self.overwrite_file = None
                
                full_path = data_dir + self.file_name + '.pkl'
                
                if self.is_load_view:
                    self.load_game(full_path) 
                else:
                    self.save_game(full_path)

            
                
                















