#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 19:27:39 2025

@author: steve
"""

import os
import pygame
import opensimplex
import numpy as np
temp_rng = np.random.RandomState()      # FIXME TEMP

import utils
import constants as const
from rotatable_image import RotatableImage



WIDTH = 1200
HEIGHT = 800



pygame.init()

#screen = pygame.display.set_mode((WIDTH,HEIGHT))

#clock = pygame.time.Clock()



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

"""
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
            #color = ( color2 * ratio ) + ( color1 * ( 1- ratio))
            
            color = utils.fade_color_to(color1, color2, ratio )
            
            # lerp(Color, float) -> Color
            
            screen.set_at((x+x_offset, y+y_offset), color)
            
"""
"""
FEATURE_SIZE = 10
LARGE = 40

A = np.zeros([size, size])
M = np.zeros([size, size])
E = np.zeros([size, size])



random.seed(44)
clamp_low = (random.random() -0.5 ) * 2
clamp_high = clamp_low + 0.1 # (random.random() +0.5 ) * 2 # random.random()  # clamp_low + 0.1
if clamp_low > clamp_high:
    clamp_low, clamp_high = clamp_high, clamp_low 




for y in range(0, size):
    for x in range(0, size):
            
        A[x,y] = opensimplex.noise2(x/FEATURE_SIZE,y/FEATURE_SIZE)
        M[x,y] = opensimplex.noise2(x/LARGE,y/LARGE)   

        E[x,y] = M[x,y] * A[x,y] 


#np.save('./moo.txt', A)

print_thing(A, x0)
print_thing(M, size + x0*2)        
print_thing(E, size*2 + x0*3)   
 
"""    

PLANET_VIEW_RADIUS_MULT = 8  # FIXME: Dup im planets
mapHeight = 100

#time = 0
#rotationSpeed = 1


BLOCK_SIZE = 400
SMALL_FEATURES = 10
LARGE_FEATURES = 40

def gen_data(data, feature_size):
    for y in range(0, BLOCK_SIZE):
        for x in range(0, BLOCK_SIZE):
            data[x,y] = opensimplex.noise2(x/feature_size,y/feature_size)

class PlanetaryTextures():
    
    def __init__(self):
        
        small_filename = './data/SmallFeatures_' + str(const.random_seed) + '.npy'
        large_filename = './data/LargeFeatures_' + str(const.random_seed) + '.npy'
        
        self.small_features = np.zeros([BLOCK_SIZE, BLOCK_SIZE])
        self.large_features = np.zeros([BLOCK_SIZE, BLOCK_SIZE])
        

        if os.path.isfile(small_filename):
            self.small_features = np.load(small_filename)
        else:
            gen_data(self.small_features, SMALL_FEATURES)
            np.save(small_filename, self.small_features)
            
        if os.path.isfile(large_filename):
            self.large_features = np.load(large_filename)
        else:
            gen_data(self.large_features, LARGE_FEATURES)       
            np.save(large_filename, self.large_features)

        self.combined_features = self.small_features * self.large_features


    def get_image(self, planet):
        
        planet_view_r = planet.size * PLANET_VIEW_RADIUS_MULT * 2
        
        TEMP_buffer = 50
        
        # FIXME: Switch to my_random
        xoffset =  temp_rng.randint(TEMP_buffer, BLOCK_SIZE - planet_view_r - TEMP_buffer)
        yoffset = temp_rng.randint(TEMP_buffer, BLOCK_SIZE - planet_view_r - TEMP_buffer)
        print(planet_view_r, xoffset, yoffset)
        surface = pygame.Surface((planet_view_r, planet_view_r), pygame.SRCALPHA)
        

        for x in range(planet_view_r):
            for y in range(planet_view_r):
    
                # convert pixel position into a vector relative to the center and normalize
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
    
                if planet.planet_type == 'earth-like':
                    value = self.large_features[int(u)+xoffset][int(v)+yoffset]
                else:
                    #print(int(u)+xoffset,int(v)+yoffset)
                    value = self.combined_features[int(u)+xoffset][int(v)+yoffset]

            
                value = ( value + 1 ) / 2 # normal
                t1 = 207
                t2 = 1 + 206 * value
                t3 = 21 * value
            
                newcolor = ( t1, t2, t3 )
            
    
                surface.set_at((x, y), newcolor)
    
    
                
        return RotatableImage(const.screen_center, surface)
"""
class Planet():
    
    def __init__(self, size):
        
        self.size = size
        self.planet_type = 'lava'

pt = PlanetaryTextures()

planet = Planet(10)
surface = pt.get_image(planet)

rot_image = RotatableImage(const.screen_center, surface)

spin = 0

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
    #surface = pt.get_image(planet)
    
    
    rot_image.angle_deg = spin
    
    rot_image.draw(screen)
    
    spin += 1
    
    pygame.display.flip()  # Refresh on-screen display
    clock.tick(24)        
          

"""




    