#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 19:14:08 2024

@author: steve
"""
import pygame
from pygame.math import Vector2
import math

screen_width = 1200
screen_height = 800

screen_center = Vector2(screen_width/2, screen_height/2)

random_seed = 43

free_space_in_corners = 20

home_xy = Vector2(screen_width - free_space_in_corners, free_space_in_corners)

num_stars = 600
num_systems = 96

planet_size_freq = [4,4,4,4,4,4,5,5,5,5,5,6,6,6,7,7,8,9,10]

ship_width = 18

our_initial_resources = {
    'credits': 0,
    'fuel': 20,
    'metal': 0,
    'tech': 0,
    'laser': math.inf,
    'cannon': 0,
    'rocket': 0,
    'torpedo': 0,
    'mine': 0
    }

their_initial_resources = {
    'credits': 10,
    'fuel': 10,
    'metal': 10,
    'tech': 10,
    'laser': math.inf,
    'cannon': 5,
    'rocket': 5,
    'torpedo': 2,
    'mine': 2
    }

initial_planetary_resources = {
    'credits': 40,
    'fuel': 8,
    'metal': 15,
    'tech': 15,
    'cannon': 2,
    'rocket': 2,
    'torpedo': 2,
    'mine': 2
    }

# of each
station_resources = 500

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
      our_capital: 1  
}

species_color = {
      neutral_capital: pygame.Color('cyan'),
      friendly_capital: pygame.Color('mediumspringgreen'),
      hostile_capital: pygame.Color('red3'),
      our_capital: pygame.Color('white')
    }


upgrade_cost_mults = [ 0, 1, 5, 10]

game_color = (255, 181, 108)

weapon_cost = {
    'cannon': 2,
    'rocket': 2,
    'torpedo': 4,
    'mine': 5    
    }

fx_rates = {}
fx_rates[neutral_capital] = {
    'fuel': 1,
    'metal': 2,
    'tech': 1,
    'cannon': weapon_cost['cannon'],
    'rocket': weapon_cost['rocket'],
    'torpedo': weapon_cost['torpedo'],
    'mine': weapon_cost['mine']
    }
fx_rates[hostile_capital] = {
    'fuel': 1,
    'metal': 1,
    'tech': 2,
    'cannon': weapon_cost['cannon']*4,
    'rocket': weapon_cost['rocket']*4,
    'torpedo': weapon_cost['torpedo']*4,
    'mine': weapon_cost['mine']*4
    }
fx_rates[friendly_capital] = {
    'fuel': 1,
    'metal': 1,
    'tech': 1,
    'cannon': weapon_cost['cannon'],
    'rocket': weapon_cost['rocket'],
    'torpedo': weapon_cost['torpedo'],
    'mine': weapon_cost['mine']
    }

weapon_hit_radius = 15

# relationship between orbital acceleration and ship speed
acc_over_speed = 1/3

# G
G = 1

# cost of armour repair
armour_per_metal = 5

# pixels per unit of fuel
distance_per_fuel = 10

# left mouse clisk
left_mouse_click = 1

# right mouse click
right_mouse_click = 3

# doubleclick delay (ms)
doubleclick_delay = 400

# fuel efficiency per engine upgrade level
fuel_efficiency = [1, 1.15, 1.3, 1.5]

# frames per second
clock_tick = 24

