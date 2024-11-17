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
import utils

SUN_SIZE_MULT = 3
MOUSE_RADIUS = 5    # FIXME: DUP in galaxy_
SYSTEM_HIGHLIGHT = 3 # FIXME: DUP in galaxy_

class SolarView(game_view.GameView):
    
    def __init__(self, screen, system, ships):
        self.system = system
        
        
        
        game_view.GameView.__init__(self, screen, ships)
        
        self.current_ship.system = system


        self.current_planet = None
        self.selected_planet = None
                
        self.mobs = [self.current_ship]
        
        for ship in self.ships:
            if ship.system == self.system:
                
                if ship.planet:
                    ship.reset_xy(ship.planet.xy)
                else:
                    ship.reset_xy(const.screen_center)
                    
                if ship.is_npc:
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
                    if self.current_planet:
                        view = planet_view.PlanetView(self.screen, self.current_planet, self.ships)
                if  event.key == pygame.K_j:   
                    if self.selected_planet:
                        self.current_ship.destination = self.selected_planet.xy
        return view
    
    def update(self):
        game_view.GameView.update(self)
    
        self.selected_planet = None
        mousepos = Vector2(pygame.mouse.get_pos())
        for planet in self.system.planets:
            if planet.xy.distance_to(mousepos) < MOUSE_RADIUS:
                self.selected_planet = planet
            if planet.xy.distance_to(self.current_ship.xy) < MOUSE_RADIUS:
                self.current_planet = planet
    
        
    
    def draw(self):
        
        game_view.GameView.draw(self)
        
        
        #pygame.draw.circle(self.screen, 'white', self.mobs[1].xy, 50)
        
        if self.selected_planet:
            pygame.draw.line(self.screen, 'white', self.current_ship.xy, self.selected_planet.xy)
            pygame.draw.circle(self.screen, 'white', self.selected_planet.xy, self.selected_planet.size+SYSTEM_HIGHLIGHT, SYSTEM_HIGHLIGHT )

        
        pygame.draw.circle(self.screen, utils.fade_to_black(self.system.color, 2, 3), const.screen_center, (self.system.r+2)*SUN_SIZE_MULT)
        pygame.draw.circle(self.screen, utils.fade_to_black(self.system.color, 1, 3), const.screen_center, (self.system.r+1)*SUN_SIZE_MULT)
        pygame.draw.circle(self.screen, self.system.color, const.screen_center, self.system.r*SUN_SIZE_MULT )
        
        for planet in self.system.planets:
            pygame.draw.circle(self.screen, 'gray', const.screen_center, planet.r, 1)
            pygame.draw.circle(self.screen, planet.color, planet.xy, planet.size)
        
        
        
        game_view.GameView.draw_objects(self)