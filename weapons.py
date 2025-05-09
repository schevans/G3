#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 12:54:41 2025

@author: steve
"""

import pygame

import utils
from bullet import Bullet


weapons_data = utils.csv_loader('./data/weapons.csv')

class Weapons():

    def __init__(self):
        
        self.data = weapons_data
        
        self.selected_weapon = 'laser'
        
        self.images = {}
        for weapon in self.data.keys():
            self.images[weapon] = pygame.image.load('./graphics/' + weapon + '.png')
        
        
    def select_from_key(self, key):
        
        weapon = list(self.data.keys())[int(key)-1]
        self.select(weapon)
        return weapon
        
    def select(self, weapon):
        self.selected_weapon = weapon
    
    def fire(self, shooter, target):

        if self.data[self.selected_weapon]['homing'] and not target:
            return None
        
        if shooter.fit('capacitor') < self.data[self.selected_weapon]['activation']:
            return None
        
        # npcs don't consume ammo
        if not shooter.is_npc:
            if shooter.resources[self.selected_weapon] <= 0:
                return None
            shooter.resources[self.selected_weapon] -= 1
            
        shooter.fit.systems['capacitor'].value -= self.data[self.selected_weapon]['activation']
            
        return Bullet(shooter, target, pygame.mouse.get_pos(), self.images[self.selected_weapon], self.data[self.selected_weapon])
        

    
    def draw_icons(self, screen, resources, size, x_offset):
        

        for weapon in self.data.keys():
            
            surface = pygame.Surface(size, pygame.SRCALPHA)
            surface.fill('black')
            
            border_color = pygame.Color('white') if weapon == self.selected_weapon else pygame.Color('gray66')
            pygame.draw.rect(surface, border_color, ((0,0), size), 2)
            
            image = self.images[weapon]
            image_rect = image.get_rect()
            image_rect.center = surface.get_rect().center
            surface.blit(self.images[weapon], image_rect)
            
            text = str(resources[weapon])
            text_surface = utils.fonts[12].render(text, True, 'white')
            surface.blit(text_surface, (3,size[1]-text_surface.get_size()[1]-3))
            
            if self.data[weapon]['homing']:
                xy = (size[0]*(3/4), size[1]*(1/4))
                pygame.draw.circle(surface, 'white', xy, 3, 1)
                pygame.draw.circle(surface, 'white', xy, 5, 1)
                pygame.draw.line(surface, 'white', xy, xy)
                #pygame.draw.line(surface, 'white', (xy[0], xy[1]-8), (xy[0], xy[1]+8))
                
            screen.blit(surface, (x_offset, 5))
            
            x_offset += size[0] + 4


    def pickle(self):
        return self.data
    
    def unpickle(self, data):
        self.data = data


















