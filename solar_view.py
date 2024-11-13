#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 17:48:27 2024

@author: steve
"""
import pygame
from pygame.math import Vector2

import game_view
import constants as const 
import galaxy_view
import planet_view
import planets
import utils

SUN_SIZE_MULT = 3

class SolarView(game_view.GameView):
    
    def __init__(self, screen, system, ships):
        self.system = system
        
        
        
        game_view.GameView.__init__(self, screen, ships)
        
        ships[0].reset_xy(const.screen_center)

        
        self.mobs = [ships[0]]
        
        self.current_planet = planets.Planet(177, 0.2, 'lava', 10 ) # FIXME
        
        for ship in self.ships:
            if ship.location.system == self.system:
                self.mobs.append(ship)
        
    def process_inputs(self):
        view = self
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
                
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_g:
                    view = galaxy_view.GalaxyView(self.screen, self.ships)
                if event.key == pygame.K_p:
                    view = planet_view.PlanetView(self.screen, self.current_planet, self.ships)
        return view
    
    def update(self):
        game_view.GameView.update(self)
    
    def draw(self):
        
        game_view.GameView.draw(self)
        
        #pygame.draw.circle(self.screen, utils.fade_to_black(system.color, 2, 3), system.xy, system.r+2)
        
        
        
        pygame.draw.circle(self.screen, utils.fade_to_black(self.system.color, 2, 3), const.screen_center, (self.system.r+2)*SUN_SIZE_MULT)
        pygame.draw.circle(self.screen, utils.fade_to_black(self.system.color, 1, 3), const.screen_center, (self.system.r+1)*SUN_SIZE_MULT)
        pygame.draw.circle(self.screen, self.system.color, const.screen_center, self.system.r*SUN_SIZE_MULT )
        
        for planet in self.system.planets:
            pygame.draw.circle(self.screen, 'gray', const.screen_center, planet.r, 1)
            pygame.draw.circle(self.screen, planet.color, planet.xy, planet.size)
        
        
        
        game_view.GameView.draw_objects(self)