#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 19:27:39 2025

@author: steve
"""

import pygame
import opensimplex
import numpy as np
import random

import utils
import constants as const
from rotatable_image import RotatableImage

WIDTH = 1200
HEIGHT = 800



pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))

clock = pygame.time.Clock()



size = 200

x0 = 50
y0 = 50


# lava
color1 = pygame.Color('yellow')
color2 = pygame.Color('brown')
lava = 10*40

# earth-like
#color1 = pygame.Color('green')
#color2 = pygame.Color('blue')
#planet = M

# ocean
#color1 = pygame.Color('lightblue')
#color2 = pygame.Color('blue')
# A*M

# rocky
#color1 = pygame.Color('brown4')
#color2 = pygame.Color('darkorange3')
# A*M


def print_array(array, x_offset, y_offset=50):
    for y in range(0, size):
        for x in range(0, size):
            
            color = (0, int((array[x,y] + 1) * 128), 0)

            screen.set_at((x+x_offset, y+y_offset), color)
            
            
def print_thing(array, x_offset, y_offset=50):
    for y in range(0, size):
        for x in range(0, size):
            
            #value = array[x,y]
            ratio = (array[x,y] + 1) / 2
            color = ( color2 * ratio ) + ( color1 * ( 1- ratio))
            
            utils.fade_color_to(color1, color2, ratio )
            
            # lerp(Color, float) -> Color
            
            screen.set_at((x+x_offset, y+y_offset), color)
            


def clamp(n, smallest, largest): return max(smallest, min(n, largest))
def butterfly(n, smallest, largest): return max(largest, min(n, smallest))

FEATURE_SIZE = 10
LARGE = 40

A = np.zeros([size, size])
M = np.zeros([size, size])
E1 = np.zeros([size, size])
E2 = np.zeros([size, size])
E3 = np.zeros([size, size])


random.seed(44)
clamp_low = (random.random() -0.5 ) * 2
clamp_high = clamp_low + 0.1 # (random.random() +0.5 ) * 2 # random.random()  # clamp_low + 0.1
if clamp_low > clamp_high:
    clamp_low, clamp_high = clamp_high, clamp_low 




for y in range(0, size):
    for x in range(0, size):
            
        A[x,y] = opensimplex.noise2(x/FEATURE_SIZE,y/FEATURE_SIZE)
        M[x,y] = opensimplex.noise2(x/LARGE,y/LARGE)   

        E1[x,y] = M[x,y] * A[x,y] 

        R = 2; # Higher for less mountains.
        A[x,y] = pow(A[x,y],R);

        P = 2   # Higher for stronger bias.  
        E2[x,y] = M[x,y] * pow(A[x,y]*2,P)/2 if A[x,y]  < 0 else 1-(pow((1-A[x,y])*2,P)/2)

        E3[x,y] = clamp(E2[x,y], clamp_low, clamp_high)



#np.save('./moo.txt', A)

print_thing(A, x0)
print_thing(M, size + x0*2)        
print_thing(E1, size*2 + x0*3)   
print_thing(E2, size*3 + x0*4)   
print_thing(E3, x0, size + y0*2 )   
    

PLANET_VIEW_RADIUS_MULT = 8  # FIXME: Dup im planets
mapHeight = 100

time = 0
rotationSpeed = 1

def get_image(planet):
    
    planet_view_r = planet.size * PLANET_VIEW_RADIUS_MULT * 2
    
    surface = pygame.Surface((planet_view_r, planet_view_r), pygame.SRCALPHA)
    
    for x in range(planet_view_r):
        for y in range(planet_view_r):

            # normalize
            px = x * 2/planet_view_r - 1
            py = y * 2/planet_view_r - 1
            
            # get the squared magnitude
            magSq = px * px + py * py
            
            # outside the circle? leave blank.
            if ( magSq > 1 ):
                continue
            
            # lens distortion
            scale = 0.35 * magSq + (1 - 0.35)
            px = px * scale
            py = py * scale
            
            # convert our local offsets into lookup coordinates into our map texture
            u = (px + 1) * (mapHeight/2) 
            v = (py + 1) * (mapHeight/2)

            
            moo = E1[int(u)][int(v)]
        
            moo = ( moo + 1 ) / 2 # normal
            t1 = 207
            t2 = 1 + 206 * moo
            t3 = 21 * moo
        
            newcolor = ( t1, t2, t3 )
        

            surface.set_at((x, y), newcolor)


            
    return surface

class Planet():
    
    def __init__(self, size):
        
        self.size = size

planet = Planet(10)
surface = get_image(planet)

rot_image = RotatableImage(const.screen_center, surface)

spin = 0

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
    surface = get_image(planet)
    
    
    rot_image.angle_deg = spin
    
    rot_image.draw(screen)
    
    spin += 1
    
    pygame.display.flip()  # Refresh on-screen display
    clock.tick(24)        
          






    