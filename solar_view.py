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

SYSTEM_HIGHLIGHT = 3 # FIXME: DUP in galaxy_

class SolarView(game_view.GameView):
    
    def __init__(self, screen, system, current_ship, ships):
        self.system = system
        
        game_view.GameView.__init__(self, screen, current_ship, ships)
        
        self.current_ship.system = system
                      
        for ship in self.ships:
            if ship.system == self.system:
                
                if ship.planet:
                    ship.reset_xy(ship.planet.xy)
                else:
                    ship.reset_xy(const.screen_center)
                    

                self.mobs.append(ship)


    def process_inputs(self):
        view = self
        
        for event in pygame.event.get():
            self.process_event(event)
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_g:
                    view = galaxy_view.GalaxyView(self.screen, self.current_ship, self.ships)
                if event.key == pygame.K_p:
                    if self.current_ship.planet:
                        view = planet_view.PlanetView(self.screen, self.current_ship.planet, self.current_ship, self.ships)
                if  event.key == pygame.K_j:   
                    if self.selected_item:
                        self.current_ship.destination = self.selected_item
        return view
    
    def update(self):
        game_view.GameView.update(self)
    
        self.get_selected_item(self.system.planets)


    def draw(self):
        
        game_view.GameView.draw(self)
        
        if self.selected_item:
            pygame.draw.line(self.screen, 'white', self.current_ship.xy, self.selected_item.xy)
            pygame.draw.circle(self.screen, 'white', self.selected_item.xy, self.selected_item.size+SYSTEM_HIGHLIGHT, SYSTEM_HIGHLIGHT )

        
        pygame.draw.circle(self.screen, utils.fade_to_black(self.system.color, 2, 3), const.screen_center, (self.system.r+2)*SUN_SIZE_MULT)
        pygame.draw.circle(self.screen, utils.fade_to_black(self.system.color, 1, 3), const.screen_center, (self.system.r+1)*SUN_SIZE_MULT)
        pygame.draw.circle(self.screen, self.system.color, const.screen_center, self.system.r*SUN_SIZE_MULT )
        
        for planet in self.system.planets:
            pygame.draw.circle(self.screen, 'gray', const.screen_center, planet.r, 1)
            pygame.draw.circle(self.screen, planet.color, planet.xy, planet.size)
        
        
        
        game_view.GameView.draw_objects(self)
        
        
    def get_mouse_text(self):
        text = []
        if self.selected_item:
            text.append(self.selected_item.description())
            for mob in self.mobs:
                if mob.planet == self.selected_item:
                    text.append(mob.description())
                    
        return text