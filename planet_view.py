#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 17:48:26 2024

@author: steve
"""
import pygame
from pygame.math import Vector2
import math

import constants as const 
import orbital_ships
import utils
import my_random
from game_view import GameView, View

DOCK_RADIUS = 15
LOCK_RADIUS = 10

LEFT_MOUSE_CLICK = 1
RIGHT_MOUSE_CLICK = 3

class PlanetView(GameView):

    def __init__(self):
        GameView.__init__(self)
        
        
    def cleanup(self):
        self.mobs = []

    def startup(self, shared_dict):
        self.shared_dict = shared_dict
        self.shared_dict['history'].append(View.PLANET)
        self.current_ship = self.shared_dict['current_ship']
        self.planet = shared_dict['planet']
        self.planet_r = self.planet.size*8
        
        angle_radians = 0
        
        applicable_mobs = []
        
        for ship in self.ships:
            if ship.planet == self.planet:
                applicable_mobs.append(ship)
           
        if applicable_mobs:
            angle_increment = ( math.pi * 2 ) / len(applicable_mobs)
            
            for mob in applicable_mobs:                                 
                angle_radians += angle_increment
                self.mobs.append(orbital_ships.OrbitalShip(mob, self.planet, self.get_random_r(), angle_radians))

        self.is_paused = False 

    def process_event(self, event):
        
        GameView.process_event(self, event)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.shared_dict['system'] = self.planet.system
                self.next_view = (View.SOLAR, self.shared_dict)
            if event.key == pygame.K_SPACE:
                self.is_paused = not self.is_paused
            if event.key == pygame.K_w:
                for mob in self.mobs:
                    if mob.name != 'Hero' and self.mobs[0].xy.distance_to(mob.xy) < DOCK_RADIUS:
                        mob.tmpship.recruit()  # FIXME: Better solution (tmpship - conjoined with orbital_ship)
                        self.shared_dict['other_ship'] = mob
                        self.next_view = (View.DOCKING, self.shared_dict)
        #if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT_MOUSE_CLICK:
        if event.type == pygame.KEYDOWN and pygame.K_TAB:
            self.lock_target()
                
                        
        keys = pygame.key.get_pressed() 
        self.mobs[0].acceleration = 0
        if keys[pygame.K_d]:
            self.mobs[0].acceleration  = 1
        if keys[pygame.K_a]:        
            self.mobs[0].acceleration  = -1  
                        
    def update(self):
        if not self.is_paused:
            GameView.update(self)
 
        self.get_selected_item(self.mobs)

    def draw(self, screen):
        
        GameView.draw(self, screen)
        pygame.draw.circle(screen, self.planet.color, const.screen_center, self.planet_r)
        GameView.draw_objects(self, screen)
        
        if self.is_paused:
            text = '[ Paused ]'
            text_surface = utils.fonts[30].render(text, True, 'white', 'black')
            text_width, text_height = text_surface.get_size()
            text_pos = Vector2(const.screen_width / 2 - text_width / 2, text_height + 10)
            screen.blit(text_surface, text_pos )
        
    def get_mouse_text(self):
        return [self.selected_item.description()]

    def get_local_allies(self):
        allies = []
        for ship in self.ships:
            if not ship.is_npc and ship.planet == self.current_ship.planet:
                allies.append(ship)
        return allies   
    
    def get_random_r(self):
        r = int(my_random.my_gauss() * ( const.screen_height/2 - self.planet_r + const.ship_width ) + 40)
        
        for mob in self.mobs:
            if math.isclose(r, mob.r, abs_tol=const.ship_width):
                return self.get_random_r()
        return r



    def lock_target(self):
        
        mousepos = pygame.mouse.get_pos()
        
        for mob in self.mobs:
            if mob.xy.distance_to(mousepos) <= LOCK_RADIUS:
                if not utils.line_intersects_circle(self.current_ship.xy, mob.xy, const.screen_center, self.planet_r):
                    self.mobs[0].target = mob
        

        




        
        
        
        