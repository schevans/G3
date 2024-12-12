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

EXPOSITION_BOX_SIZE = 100

class ExpositionText(Enum):
    OPENING = 1
    
       


class ExpositionBox():
    
    text_filenames = {
        ExpositionText.OPENING: 'story/opening.txt'
        } 
        

    def __init__(self, text_enum, callback):

        
        self.surface = pygame.Surface((const.screen_width, const.screen_height), pygame.SRCALPHA)

        # FIXME: Note 30 is is the same as in button above. Abstracify        
        button_pos = Vector2(const.screen_width / 2 - 100 / 2, const.screen_height - EXPOSITION_BOX_SIZE - 30 - 30)
        self.button = Button(button_pos, (100,30), 'OK', const.game_color, None, False, callback)
        
        
        filename = ExpositionBox.text_filenames[text_enum]
        self.text = []
        with open(filename) as file:
            for line in file.readlines():
                #line = line.strip('\n')
                self.text.append(line.strip('\n'))

        self.font = utils.fonts[20]
        
        
    def process_event(self, event):
        
        self.button.process_event(event)
        
    def update(self):
        self.button.update()
    
    def draw(self, screen):   

        # inner text box
        inner_rect = pygame.Rect(EXPOSITION_BOX_SIZE, EXPOSITION_BOX_SIZE, const.screen_width - 2*EXPOSITION_BOX_SIZE, const.screen_height - 2*EXPOSITION_BOX_SIZE)
        pygame.draw.rect(self.surface, pygame.Color(0,0,0,255), inner_rect) 
    
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

        #textbox_width, textbox_height = utils.get_required_textbox_size(self.text, self.font)
        
        text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
        
        text_arr = []
        sentence = ''
        word_arr = text.split(' ')
        
        for word in word_arr:
            if self.font.size(sentence + word + ' ')[0] <= inner_rect[2] - 10:
                sentence = sentence + word + ' '
            else:
                text_arr.append(sentence)
                sentence = word

        
        self.text = text_arr
        
        offset = EXPOSITION_BOX_SIZE + border + 10
        font_height = self.font.size(self.text[0])[1]
        for i in range(0, len(self.text)):
            text_surface = self.font.render(self.text[i], True, 'white', 'black')
            self.surface.blit(text_surface,  (offset, offset + font_height * (i)))
        

        screen.blit(self.surface,(0,0))

        
            
            
        