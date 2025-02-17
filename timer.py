#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 20:56:52 2025

@author: steve
"""

import pygame

class Timer():
    
    def __init__(self):
        
        self.start_time = 0
        
        
    def get_next_second(self):
        
        if self.start_time == 0:
            self.start_time = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.start_time > 1000:
            self.start_time = 0
            return True
        else:
            return False
        
    def get_next_ms_interval(self, ms_interval):
        
        if self.start_time == 0:
            self.start_time = pygame.time.get_ticks()

        if pygame.time.get_ticks() - self.start_time > ms_interval:
            self.start_time = 0
            return True
        else:
            return False
        



        
        