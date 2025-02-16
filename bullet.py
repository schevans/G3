#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 17:14:47 2025

@author: steve
"""
from pygame.math import Vector2

class Bullet():
    
    def __init__(self, selected_weapon):
        
        self.xy = Vector2(33, 55)
    
    
    def update(self):
        pass
    
    def draw(self, screen):
        print('bullet')
        pass
    
    def item_type(self):
        return 'Bullet'
    