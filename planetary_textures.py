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

import utils
import constants as const
from rotatable_image import RotatableImage
import my_random

opensimplex.seed(const.random_seed)

PLANET_VIEW_RADIUS_MULT = 8  # FIXME: Dup im planets
MAP_HEIGHT = 100
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
            print('First time planetary texture generation for seed ' + str(const.random_seed) + '...')
            gen_data(self.small_features, SMALL_FEATURES)
            print('...')
            np.save(small_filename, self.small_features)
            
        if os.path.isfile(large_filename):
            self.large_features = np.load(large_filename)
        else:
            gen_data(self.large_features, LARGE_FEATURES)       
            np.save(large_filename, self.large_features)
            print('Done.')

        self.combined_features = self.small_features * self.large_features


    def get_image(self, planet):
        
        planet_view_r = planet.size * PLANET_VIEW_RADIUS_MULT * 2
        
        surface = pygame.Surface((planet_view_r, planet_view_r), pygame.SRCALPHA)
        
        buffer = 50

        xoffset =  my_random.my_randint(buffer, BLOCK_SIZE - planet_view_r - buffer)
        yoffset = my_random.my_randint(buffer, BLOCK_SIZE - planet_view_r - buffer)

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
                u = (px + 1) * (MAP_HEIGHT/2) 
                v = (py + 1) * (MAP_HEIGHT/2)
    
                if planet.planet_type == 'earth-like':
                    value = self.large_features[int(u)+xoffset][int(v)+yoffset]
                else:
                    value = self.combined_features[int(u)+xoffset][int(v)+yoffset]

                value = ( value + 1 ) / 2 # normal
                color = utils.fade_color_to(planet.color1, planet.color2, value)
    
                surface.set_at((x, y), color)
            
        small_image = pygame.transform.scale_by(surface, 1/PLANET_VIEW_RADIUS_MULT)
        
        return (RotatableImage(const.screen_center, surface), RotatableImage(planet.xy, small_image))







    