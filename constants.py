#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 19:14:08 2024

@author: steve
"""
from pygame.math import Vector2

screen_width = 1200
screen_height = 800

screen_center = Vector2(screen_width/2, screen_height/2)

random_seed = 43

free_space_in_corners = 20

home = Vector2(screen_width - free_space_in_corners, free_space_in_corners)

num_stars = 600
num_systems = 97

planet_size_freq = [4,4,4,4,4,4,5,5,5,5,5,6,6,6,7,7,8,9,10]

initial_resources = {
    'credits': 10,
    'fuel': 300,
    'metal': 10,
    'tech': 10
    }

system_types = ['Uninhabited', 'Neutral', 'Friendly', 'Hostile']

species = {
      'Neutral': 'Neuties',
      'Friendly': 'Goodies',
      'Hostile': 'Baddies',
      'Home': 'Polarians'
    }


