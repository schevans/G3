#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 17:46:52 2024

@author: steve
"""
import pygame
import random

import ships
import systems
import constants as const
import utils
import galaxy_view


random.seed(43)

pygame.init()

screen = pygame.display.set_mode((const.screen_width, const.screen_height))

clock = pygame.time.Clock()

pygame.font.init() 

font = pygame.font.SysFont('Comic Sans MS', 20)


    

utils.init_stars(const.num_stars)
systems.init_systems(const.num_systems)




hero_name = 'Hero'

myship = ships.Ship(hero_name, (const.free_space_in_corners,const.screen_height-const.free_space_in_corners), None, None, False)



shiplist = [ myship ]

for system in systems.syslist:
    if system.system_type != 'Uninhabited':
        planet = system.planets[random.randint(0, len(system.planets)-1)]
        shiplist.append(ships.Ship(system.name, system.xy, system, planet, True))




view = galaxy_view.GalaxyView(screen, shiplist)



while True:
    
    # Process player inputs.
    view = view.process_inputs()
           
 

    # Do logical updates here.
    # AI

    # then
    # Physics
    view.update()  
    
    # Render the graphics here.
    view.draw()

    #print(view.master_timer)
    
    pygame.display.flip()  # Refresh on-screen display
    clock.tick(24)