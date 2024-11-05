#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 17:46:52 2024

@author: steve
"""
import pygame

import ship

WIDTH = 600
HEIGHT = 400
CENTER = [WIDTH/2, HEIGHT/2]

pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))

clock = pygame.time.Clock()

pygame.font.init() 

font = pygame.font.SysFont('Comic Sans MS', 20)

myship = ship.Ship((200,200),False)

things = [ myship ]

while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
         
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_d]:
        myship.heading += 10
    if keys[pygame.K_a]:      
        myship.heading -= 10  
         
    # Do logical updates here.
    # AI

    # then
    # Physics
    for thing in things:
        thing.update()
        
    # Render the graphics here.
    screen.fill('black')
    for thing in things:
        thing.draw(screen)
        
            
    pygame.display.flip()  # Refresh on-screen display
    clock.tick(24)