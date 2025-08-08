#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 18:24:44 2024

@author: steve
"""

import pygame
from pygame import Vector2
from enum import Enum
import json

import constants as const
from gui import Button, CheckBox
import utils
import my_random


MAX_BOX_BORDER = 100


MAX_BOX_WIDTH = 1000
MAX_BOX_HEIGHT = 600



MIN_BOX_WIDTH = 800
MIN_BOX_HEIGHT = 140


increment = 5.5

class ExpositionText(Enum):
    OPENING = 'OPENING'
    NO = 'NO'
    YES = 'YES'
    NO_THANKS = 'NO_THANKS'
    FIRST_HOSTILE = 'FIRST_HOSTILE'
    FIRST_NEUTRAL = 'FIRST_NEUTRAL'
    FIRST_FRIENDLY = 'FIRST_FRIENDLY'
    FIRST_UNINHABITED = 'FIRST_UNINHABITED'
    FIRST_SISTERS = 'FIRST_SISTERS'
    FIRST_COMBAT = 'FIRST_COMBAT'
    FIRST_COMBAT_WITH_ALLIES = 'FIRST_COMBAT_WITH_ALLIES'
    FIRST_ENEMY_LAUNCH = 'FIRST_ENEMY_LAUNCH'
    FIRST_ENEMY_LAND = 'FIRST_ENEMY_LAND'
    FINAL_BATTLE = 'FINAL_BATTLE'
    FINAL_BATTLE_WITH_ALLIES = 'FINAL_BATTLE_WITH_ALLIES'
    FIRST_RECRUIT = 'FIRST_RECRUIT'
    FIRST_PLANET = 'FIRST_PLANET'
    FIRST_BATTLE_WITH_ALLIES = 'FIRST_BATTLE_WITH_ALLIES'


# load exposition
opening_exposition_filename = 'story/opening.txt'

events_exposition = {}
with open('./story/events.json') as f:
     events_exposition = json.load(f)

expo_recruit = {}
expo_recruit[ExpositionText.YES] = {}
expo_recruit[ExpositionText.NO_THANKS] = {}
expo_recruit[ExpositionText.NO] = {}

with open('./story/expo_recruit_yes.json') as f:
     expo_recruit[ExpositionText.YES] = json.load(f)
with open('./story/expo_recruit_no_thanks.json') as f:
     expo_recruit[ExpositionText.NO_THANKS] = json.load(f)
with open('./story/expo_recruit_no.json') as f:
     expo_recruit[ExpositionText.NO] = json.load(f)
     
     
class ExpositionBox():   

    def __init__(self, text_enum, ok_callback, checkbox_callback, show_help_checkbox=True):
        self.checkbox_callback = checkbox_callback
        self.font = utils.fonts[20]
        self.is_help = True
        
        self.surface = pygame.Surface((const.screen_width, const.screen_height), pygame.SRCALPHA)
        
        borders = 10*4
        button_width = 100
        button_height = 30
        
        # read-and-wrap
        self.text = []
        if text_enum == ExpositionText.OPENING:
            with open(opening_exposition_filename) as file:
                for line in file.readlines():
                    line = line.strip('\n')
                    if self.font.size(line)[0] > MAX_BOX_WIDTH - borders:
                        wrapped_lines = self.wrap_text(line, MAX_BOX_WIDTH - borders)
                        self.text += wrapped_lines
                    else:
                        self.text.append(line)
        
        elif text_enum in [ExpositionText.YES, ExpositionText.NO, ExpositionText.NO_THANKS]:
            self.is_help = False  
            line = expo_recruit[text_enum][self.get_random_key(expo_recruit[text_enum])]
            if self.font.size(line)[0] > MAX_BOX_WIDTH - borders:
                wrapped_lines = self.wrap_text(line, MAX_BOX_WIDTH - borders)
                self.text += wrapped_lines
            else:
                self.text.append(line)          
            
        else: # is events_exposition
            exposition_text = events_exposition[text_enum.value].split('\n')
            for line in exposition_text:
                if self.font.size(line)[0] > MAX_BOX_WIDTH - borders:
                    wrapped_lines = self.wrap_text(line, MAX_BOX_WIDTH - borders)
                    self.text += wrapped_lines
                else:
                    self.text.append(line)
        
        # measure
        text_width = 0
        text_height = 0
        for line in self.text:
            text_width = max(text_width, self.font.size(line)[0])    
            text_height += self.font.size(line)[1]
        
        # paging
        self.current_page = 1
        if text_height > MAX_BOX_HEIGHT - (borders + button_height*2):
            self.text = self.page_text(self.text, MAX_BOX_HEIGHT - (borders + button_height*2))     
        else:
            self.text = [self.text]
        self.pages = len(self.text)
        
        self.text_color = []
        for page in self.text:
            temp = []
            for sentence in page:
                temp.append(pygame.Color('black'))
            self.text_color.append(temp)
                
        
        button_label = 'OK'
        self.old_ok_callback = ok_callback
        if self.pages > 1:
            ok_callback = self.ok_callback_intercept
            button_label = 'More..'
            
        # rect & button & checkbox
        inner_width = max(MIN_BOX_WIDTH, text_width + borders)
        inner_height = max(MIN_BOX_HEIGHT, min(text_height + 3*button_height, MAX_BOX_HEIGHT))
        
        self.inner_rect = pygame.Rect(((const.screen_width - inner_width)/2, (const.screen_height - inner_height)/2), (inner_width, inner_height))

        button_pos = Vector2(const.screen_width / 2 - button_width / 2, self.inner_rect[1]+self.inner_rect[3] -button_height*2 )
        self.button = Button(button_pos, (100,30), button_label, const.game_color, None, False, ok_callback)
        
        self.checkbox = None
        if show_help_checkbox:
            checkbox_pos = Vector2(self.inner_rect[0] + borders/2, self.inner_rect[1]  + self.inner_rect[3] - borders)
            self.checkbox = CheckBox(checkbox_pos, (20, 20), 'Show Help', const.game_color, True, self.checkbox_callback)
        
        
    def ok_callback_intercept(self, button):
        
        if self.current_page >= self.pages:
            self.old_ok_callback(button)
        else:
            self.current_page += 1
            if self.current_page >= self.pages:
                self.button.text = 'OK'
    
        
    def page_text(self, sentence_arr, height):
        
        result = []
        page = []
        for sentence in sentence_arr:
            if self.font.size(sentence)[1] * (len(page) + 1) <= height:
                page.append(sentence)
            else:
                result.append(page)
                if sentence != '':
                    page = [sentence]

        result.append(page)
    
        return result
    
    
    def wrap_text(self, text, width):
        
        text_arr = []
        sentence = ''
        word_arr = text.split(' ')
        for word in word_arr:
            if self.font.size(sentence + word + ' ')[0] <= width:
                sentence = sentence + word + ' '
            else:
                text_arr.append(sentence)
                sentence = word + ' '
        text_arr.append(sentence)
        
        return text_arr
    
        
    def process_event(self, event):
        
        self.button.process_event(event)
        
        if self.checkbox:
            self.checkbox.process_event(event)
        
    def update(self):
        
        self.button.update()
        
        # text fade-in
        for i in range(0, len(self.text[self.current_page-1])):            
            if self.text_color[self.current_page-1][i][0] < 255:
                self.text_color[self.current_page-1][i] = self.white_fade(self.text_color[self.current_page-1][i])
                break
            
        # enable button once text is rendered
        if self.text_color[self.current_page-1][-1][0] < 220:
            self.button.is_disabled = True
        else:
            self.button.is_disabled = False
    
    def white_fade(self, color):

        return tuple([min(255, rgb + increment) for rgb in list(color)])
    
    
    def draw(self, screen):   

        inner_rect = self.inner_rect.copy()
        

        # inner text box
        pygame.draw.rect(self.surface, pygame.Color(0,0,0,255), self.inner_rect) 
    
        
        # border
        border = 10
        
        pygame.draw.rect(self.surface, const.game_color, inner_rect, 1)
        inner_rect[0] += border
        inner_rect[1] += border
        inner_rect[2] -= border*2
        inner_rect[3] -= border*2
        pygame.draw.rect(self.surface, const.game_color, inner_rect, 1)
        
        
        # button
        self.button.draw(self.surface)

        
        # text
        # first, correct for the border and button
        inner_rect[0] += border
        inner_rect[1] += border
        inner_rect[2] -= border*2
        inner_rect[3] -= border + self.button.size[1]*2 

        display_text = self.text[self.current_page-1]
        colors = self.text_color[self.current_page-1]

        (text_width, text_height) = self.font.size(display_text[0])
        
        y_offset = inner_rect[1]
        x_offset = inner_rect[0]
        if len(display_text) == 1:
            x_offset = const.screen_width/2 - text_width/2

        for i in range(0, len(display_text)):
            text_surface = self.font.render(display_text[i], True, pygame.Color(colors[i]), 'black')
            self.surface.blit(text_surface,  (x_offset, y_offset + text_height * (i)))
        
        # checkbox
        if self.checkbox:
            self.checkbox.draw(self.surface)
        
        screen.blit(self.surface,(0,0))


    def get_random_key(self, expo_dict):
        
        return my_random.my_choices(list(expo_dict.keys()))[0]


            
        