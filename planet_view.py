#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 17:48:26 2024

@author: steve
"""
import pygame
from pygame.math import Vector2

import game_view
import constants as const 
import galaxy_view
import solar_view
import orbital_ships

class PlanetView(game_view.GameView):
    
    def __init__(self, screen, planet, ships):
        self.planet = planet
        
        game_view.GameView.__init__(self, screen, ships)
        
        
        ships[0].reset_xy((const.screen_width/2, const.screen_height/5))
        ships[0].planet = planet
        
        moo = orbital_ships.OrbitalShip(ships[0], 150, 90)
        
        self.mobs = [moo]
        
        
        """
        for ship in self.ships:
            if ship.planet == self.planet:
                self.mobs.append(ship)
        """        
                
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