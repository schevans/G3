#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 17:48:26 2024

@author: steve
"""
import pygame
from pygame.math import Vector2
import math

import game_view
import constants as const 
import galaxy_view
import solar_view
import orbital_ships

DOCK_RADIUS = 15

class PlanetView(game_view.GameView):
    
    def __init__(self, screen, planet, ships):
        self.planet = planet
        
        game_view.GameView.__init__(self, screen, ships)
        

        ships[0].planet = planet
        

        angle_radians = 0
        self.mobs = [orbital_ships.OrbitalShip(ships[0], planet, 150, angle_radians)]
        
        
        applicable_mobs = []
        
        for ship in self.ships:
            if ship.planet == self.planet and ship.is_npc:
                applicable_mobs.append(ship)
                
        angle_increment = math.pi / len(applicable_mobs)
        
        for mob in applicable_mobs:
                               
            if ship.is_npc:
                angle_radians += angle_increment
                self.mobs.append(orbital_ships.OrbitalShip(ship, planet, 150, angle_radians))

                
                
    def process_inputs(self):
        
        view = self
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    view = solar_view.SolarView(self.screen, self.planet.system, self.ships)
                if event.key == pygame.K_g:
                    view = galaxy_view.GalaxyView(self.screen, self.ships)
                if event.key == pygame.K_w:
                    for mob in self.mobs:
                        if mob.name != 'Hero' and self.mobs[0].xy.distance_to(mob.xy) < DOCK_RADIUS:
                            print('Docked! Star-Lord', mob.name )
                            mob.is_npc = False
                       
        keys = pygame.key.get_pressed() 
        self.mobs[0].acceleration = 0
        if keys[pygame.K_d]:
            self.mobs[0].acceleration  = 1
        if keys[pygame.K_a]:        
            self.mobs[0].acceleration  = -1  
                

        return view 
    
    def update(self):
        game_view.GameView.update(self)
    
    def draw(self):      
        game_view.GameView.draw(self)
        pygame.draw.circle(self.screen, self.planet.color, const.screen_center, self.planet.size*8)
        game_view.GameView.draw_objects(self)