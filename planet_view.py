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
import utils
from game_view import GameView, View

DOCK_RADIUS = 15

class PlanetView(GameView):

    def __init__(self):
        GameView.__init__(self)

    def cleanup(self):
        self.mobs = []

    def startup(self, planet):
        self.planet = planet

        angle_radians = 0
        
        applicable_mobs = []
        
        for ship in self.ships:
            if ship.planet == self.planet:
                applicable_mobs.append(ship)
           
        if applicable_mobs:
            angle_increment = ( math.pi * 2 ) / len(applicable_mobs)
            
            for mob in applicable_mobs:                                 
                angle_radians += angle_increment
                self.mobs.append(orbital_ships.OrbitalShip(mob, planet, 150, angle_radians))

        self.is_paused = False 

    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.next_view = (View.SOLAR, self.planet.system)
            if event.key == pygame.K_SPACE:
                self.is_paused = not self.is_paused
            if event.key == pygame.K_w:
                for mob in self.mobs:
                    if mob.name != 'Hero' and self.mobs[0].xy.distance_to(mob.xy) < DOCK_RADIUS:
                        mob.is_npc = False
                        mob.liege = 'Hero'
                        mob.tmpship.is_npc = False  # FIXME: Better solution
                        mob.tmpship.liege = 'Hero'
                        
    def update(self):
        if not self.is_paused:
            game_view.GameView.update(self)
 
        self.get_selected_item(self.mobs)

    def draw(self, screen):
        
        GameView.draw(self, screen)
        pygame.draw.circle(screen, self.planet.color, const.screen_center, self.planet.size*8)
        game_view.GameView.draw_objects(self, screen)
        
        if self.is_paused:
            text = '[ Paused ]'
            text_surface = utils.fonts[30].render(text, True, 'white', 'black')
            text_width, text_height = text_surface.get_size()
            text_pos = Vector2(const.screen_width / 2 - text_width / 2, text_height + 10)
            screen.blit(text_surface, text_pos )
        
    def get_mouse_text(self):
        return [self.selected_item.description()]



class PlanetView2(game_view.GameView):
    
    def __init__(self, screen, planet, current_ship, ships):
        self.planet = planet
        
        game_view.GameView.__init__(self, screen, current_ship, ships)
    
        angle_radians = 0
        
        applicable_mobs = []
        
        for ship in self.ships:
            if ship.planet == self.planet:
                applicable_mobs.append(ship)
           
        if applicable_mobs:
            angle_increment = ( math.pi * 2 ) / len(applicable_mobs)
            
            for mob in applicable_mobs:                                 
                angle_radians += angle_increment
                self.mobs.append(orbital_ships.OrbitalShip(mob, planet, 150, angle_radians))

        self.is_paused = False      
                
    def process_inputs(self):
        
        view = self
        
        for event in pygame.event.get():
            self.process_event(event)
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    view = solar_view.SolarView(self.screen, self.planet.system, self.current_ship, self.ships)
                if event.key == pygame.K_g:
                    view = galaxy_view.GalaxyView(self.screen, self.current_ship, self.ships)
                if event.key == pygame.K_SPACE:
                    self.is_paused = not self.is_paused
                if event.key == pygame.K_w:
                    for mob in self.mobs:
                        if mob.name != 'Hero' and self.mobs[0].xy.distance_to(mob.xy) < DOCK_RADIUS:
                            mob.is_npc = False
                            mob.liege = 'Hero'
                            mob.tmpship.is_npc = False  # FIXME: Better solution
                            mob.tmpship.liege = 'Hero'
                            
        keys = pygame.key.get_pressed() 
        self.mobs[0].acceleration = 0
        if keys[pygame.K_d]:
            self.mobs[0].acceleration  = 1
        if keys[pygame.K_a]:        
            self.mobs[0].acceleration  = -1  
                

        return view 
    
    def update(self):
        
        if not self.is_paused:
            game_view.GameView.update(self)
 
        self.get_selected_item(self.mobs)
    
    def draw(self):      
        game_view.GameView.draw(self)
        pygame.draw.circle(self.screen, self.planet.color, const.screen_center, self.planet.size*8)
        game_view.GameView.draw_objects(self)
        
        if self.is_paused:
            text = '[ Paused ]'
            text_surface = utils.fonts[30].render(text, True, 'white', 'black')
            text_width, text_height = text_surface.get_size()
            text_pos = Vector2(const.screen_width / 2 - text_width / 2, text_height + 10)
            self.screen.blit(text_surface, text_pos )
        
    def get_mouse_text(self):
        return [self.selected_item.description()]
        
        
        
        
        
        
        
        
        