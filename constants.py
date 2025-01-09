#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 19:14:08 2024

@author: steve
"""
import pygame
from pygame.math import Vector2

screen_width = 1200
screen_height = 800

screen_center = Vector2(screen_width/2, screen_height/2)

random_seed = 43

free_space_in_corners = 20

home = Vector2(screen_width - free_space_in_corners, free_space_in_corners)

num_stars = 600
num_systems = 96

planet_size_freq = [4,4,4,4,4,4,5,5,5,5,5,6,6,6,7,7,8,9,10]

ship_width = 18

initial_resources = {
    'credits': 30,
    'fuel': 300,
    'metal': 10,
    'tech': 10
    }

system_types = ['Uninhabited', 'Neutral', 'Friendly', 'Hostile']

our_capital = 'Polaris'
neutral_capital = 'Alcor'
friendly_capital = 'Castor'
hostile_capital = 'Zaurak'

species = {
      'Neutral': neutral_capital,
      'Friendly': friendly_capital,
      'Hostile': hostile_capital,
      'Home': our_capital
    }

ship_image_number = {
      neutral_capital: 3,
      friendly_capital: 2,
      hostile_capital: 5,
      'Home': 1  
}

species_color = {
      neutral_capital: pygame.Color('cyan'),
      friendly_capital: pygame.Color('mediumspringgreen'),
      hostile_capital: pygame.Color('red3'),
      our_capital: pygame.Color('turquoise2')
    }


upgrade_cost_mults = [ 0, 1, 5, 10]

game_color = (255, 181, 108)

fx_rates = {}
fx_rates[neutral_capital] = {
    'fuel': 1,
    'metal': 2,
    'tech': 1
    }
fx_rates[hostile_capital] = {
    'fuel': 1,
    'metal': 1,
    'tech': 2
    }
fx_rates[friendly_capital] = {
    'fuel': 1,
    'metal': 1,
    'tech': 1
    }




