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
import systems

class PlanetView(game_view.GameView):
    
    def __init__(self, screen, planet, ships):
        self.planet = planet
        
        game_view.GameView.__init__(self, screen, ships)
        
        
        self.current_system = systems.syslist[0]
        
        ships[0].xy = Vector2(const.screen_width/2, const.screen_height/5)
        self.mobs = [ships[0]]
        for ship in self.ships:
            if ship.location.planet == self.planet:
                self.mobs.append(ship)
                
                
    def process_inputs(self):
        
        view = self
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    view = solar_view.SolarView(self.screen, self.current_system, self.ships)
                if event.key == pygame.K_g:
                    view = galaxy_view.GalaxyView(self.screen, self.ships)

        return view 
    
    def update(self):
        game_view.GameView.update(self)
    
    def draw(self):      
        game_view.GameView.draw(self)
        pygame.draw.circle(self.screen, 'darkgreen', const.screen_center, self.planet.size*8)
        game_view.GameView.draw_objects(self)