#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 18:24:44 2024

@author: steve
"""

import pygame
from pygame import Vector2
from enum import Enum

import constants as const
from gui import Button
import utils

MAX_BOX_BORDER = 100


MAX_BOX_WIDTH = 1000
MAX_BOX_HEIGHT = 600



MIN_BOX_WIDTH = 800
MIN_BOX_HEIGHT = 140




class ExpositionText(Enum):
    OPENING = 1
    A = 2
    B = 3
    C = 4
    D = 5
    E = 6  


class ExpositionBox():
    
    text_filenames = {
        ExpositionText.OPENING: 'story/opening.txt',
        ExpositionText.A: 'story/l5w.txt',
        ExpositionText.B: 'story/l15w.txt',
        ExpositionText.C: 'story/l60w.txt',
        ExpositionText.D: 'story/l1p.txt',
        ExpositionText.D: 'story/lall.txt'
        } 
        

    def __init__(self, text_enum, callback):

        
        self.font = utils.fonts[20]

        self.surface = pygame.Surface((const.screen_width, const.screen_height), pygame.SRCALPHA)
        
        borders = 10*4
        button_width = 100
        button_height = 30
        
        # read-and-wrap
        filename = ExpositionBox.text_filenames[text_enum]
        self.text = []
        with open(filename) as file:
            for line in file.readlines():
                line = line.strip('\n')
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
            self.text = self.page_text(self.text, MAX_BOX_HEIGHT - (borders + button_height))     
        else:
            self.text = [self.text]
        self.pages = len(self.text)
        
        button_label = 'OK'
        self.old_callback = callback
        if self.pages > 1:
            callback = self.callback_intercept
            button_label = 'More..'
            
        # rect & button
        inner_width = max(MIN_BOX_WIDTH, text_width + borders)
        inner_height = max(MIN_BOX_HEIGHT, min(text_height + 2*button_height, MAX_BOX_HEIGHT))
        
        self.inner_rect = pygame.Rect(((const.screen_width - inner_width)/2, (const.screen_height - inner_height)/2), (inner_width, inner_height))

        button_pos = Vector2(const.screen_width / 2 - button_width / 2, self.inner_rect[1]+self.inner_rect[3] -button_height*2 )
        self.button = Button(button_pos, (100,30), button_label, const.game_color, None, False, callback)
        
    def callback_intercept(self, button):
        
        if self.current_page >= self.pages:
            self.old_callback(button)
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
        
    def update(self):
        self.button.update()
    
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

        spacer = 10
        x_offset = inner_rect[0]
        y_offset = inner_rect[1] + border + spacer
        font_height = self.font.size(display_text[0])[1]
        for i in range(0, len(display_text)):
            text_surface = self.font.render(display_text[i], True, 'white', 'black')
            self.surface.blit(text_surface,  (x_offset, y_offset + font_height * (i)))
        
        screen.blit(self.surface,(0,0))


            
            
        