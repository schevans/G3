#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 18:06:16 2024

@author: steve
"""

import pygame
from pygame.math import Vector2
import my_random
import math
import csv

import constants as const


def angle_between_points(v1,v2):
    return math.degrees(math.atan2(v1.x - v2.x, v1.y - v2.y))

def fade_to_black(color, i, num_steps):
    
    # FIXME: Really?    
    color0 = color[0] / (num_steps + 1) * (num_steps + 1 - i )
    color1 = color[1] / (num_steps + 1) * (num_steps + 1 - i )
    color2 = color[2] / (num_steps + 1) * (num_steps + 1 - i )
    return (color0, color1, color2)


def whiten_a_bit(color, a_bit):
    # FIXME: Again, really???
    color0 = color[0]  + (( 255 - color[0] ) * a_bit)
    color1 = color[1]  + (( 255 - color[1] ) * a_bit)
    color2 = color[2]  + (( 255 - color[2] ) * a_bit)
    return (color0, color1, color2)    

stars = []

def init_stars(num_stars):
    for i in range(0,num_stars):
        randpos = Vector2(my_random.my_randint(1, const.screen_width), my_random.my_randint(1, const.screen_height))
        stars.append(randpos)



def draw_stars(screen):
    for star in stars:
        pygame.draw.circle(screen, 'white', star, 1)  




class MaxableAmount():
    
    def __init__(self, max_amount, amount=None):
        self.max = max_amount
        self.amount = amount if amount else max_amount
        
    def dec(self, change):      
        if self.amount >= change:
            self.amount -= change
            return True
        else:
            return False
        
    def inc(self, change):       
        self.amount = min(self.max, self.amount + change)
    
    def inc_max(self, max_amount, fill):
        self.max = max_amount
        if fill:
            self.amount = self.max
        
    def __call__(self):
        return self.amount

class Location():

    def __init__(self, galaxy_xy, system, planet):      
        self.galaxy_xy = Vector2(galaxy_xy)
        self.system = system
        self.planet = planet
        
        
        
def dict_loader():
    file = './data/ship_systems.csv'
    with open(file, newline='') as csvfile:

        filereader = csv.reader(csvfile, delimiter=',')

        header = next(filereader)
        for row in filereader:
            arr = row.split(',')
 

pygame.font.init()
font_dir = 'Days'    
font_name = 'Days'
font_file = './fonts/'+ font_dir + '/' + font_name + '.otf'

fonts = {
       20: pygame.font.Font(font_file, 20),
       30: pygame.font.Font(font_file, 30),
       100: pygame.font.Font(font_file, 100)
   } 
        

def numbers_to_roman(i):
    if i == 1:
        return 'I'
    elif i == 2:
        return 'II'
    elif i == 3:
        return 'III'
    elif i == 4:
        return 'IV'






