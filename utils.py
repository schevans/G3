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
import collections


import constants as const


def angle_between_points(v1,v2):
    return math.degrees(math.atan2(v1.x - v2.x, v1.y - v2.y))


def fade_color_to(current_color, fade_to_color, ratio):    
    return pygame.Color(tuple((1-ratio)*x for x in current_color)) + pygame.Color(tuple(ratio*x for x in fade_to_color))
     

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
        
        
        
def csv_loader(filename):
    
    output = collections.defaultdict(dict)
    
    with open(filename, newline='') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',')
        header = next(filereader)
        for row in filereader:
            for col in range(1, len(row)):
                output[row[0]][header[col]] = float(row[col])
                
    return output


pygame.font.init()
font_dir = 'Days'    
font_name = 'Days'
font_file = './fonts/'+ font_dir + '/' + font_name + '.otf'

fonts = {
    12: pygame.font.Font(font_file, 12),
    14: pygame.font.Font(font_file, 14),
    20: pygame.font.Font(font_file, 20),
    30: pygame.font.Font(font_file, 30),
    100: pygame.font.Font(font_file, 100)
   } 
        

def numbers_to_roman(i):
    if i == 0:
        return 'I'
    elif i == 1:
        return 'II'
    elif i == 2:
        return 'III'
    elif i == 3:
        return 'IV'


def scale_and_monochrome_ship_image(ship):
    
    ship_image = ship.image_still.original_image.copy()
    
    width, height = ship_image.get_size()
    for x in range(width):
        for y in range(height):
            
            red, green, blue, alpha = ship_image.get_at((x, y))
            
            if red < 10 and green < 10 and blue < 10:
                ship_image.set_at((x, y), pygame.Color(0, 0, 0, alpha))
            else:
                 ship_image.set_at((x, y), pygame.Color(25, 25, 25, alpha))
                      
    return pygame.transform.scale_by(ship_image, const.screen_height/height)
    

def get_random_r(body_r, object_r, object_collection, fuzz=40):
    
    r = body_r + my_random.my_gauss() * (const.screen_height/2 - body_r)
    
    for obj in object_collection:
        if math.isclose(r, obj.r, abs_tol=(object_r + fuzz*my_random.my_random())):
            return get_random_r(body_r, object_r, object_collection, fuzz)
    return r
    



