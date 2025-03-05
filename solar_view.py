#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 17:48:27 2024

@author: steve
"""
import pygame

import constants as const 
import utils

from game_view import GameView, View

SUN_SIZE_MULT = 3   
SYSTEM_HIGHLIGHT = 3 # FIXME: DUP in galaxy_
  
  
class SolarView(GameView):
    
    def __init__(self):
        GameView.__init__(self)   
        
        self.system = None
        
    def cleanup(self):
        self.mobs = []
        
    def startup(self, shared_dict):  
        self.shared_dict = shared_dict
        self.shared_dict['history'].append(View.SOLAR)
        self.current_ship = self.shared_dict['current_ship']
        self.system = shared_dict['system']

        for ship in self.ships:
            if ship.system == self.system:
                
                if ship.planet:
                    ship.reset_xy(ship.planet.xy)
                else:
                    ship.reset_xy(const.screen_center)
                    

                self.mobs.append(ship)
        
    def process_event(self, event):
        
        GameView.process_event(self, event)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                self.shared_dict['system'] = self.system
                self.next_view = (View.GALAXY, self.shared_dict)
            if event.key == pygame.K_p:
                if self.current_ship.planet and not self.current_ship.is_moving():
                    self.current_ship.destination = None
                    self.shared_dict['planet'] = self.current_ship.planet
                    self.next_view = (View.PLANET, self.shared_dict)
            if  event.key == pygame.K_j:   
                if self.selected_item:
                    self.current_ship.destination = self.selected_item       
            if event.key == pygame.K_LEFTBRACKET or event.key == pygame.K_RIGHTBRACKET:  
                self.current_ship = self.do_ship_swap(self.current_ship, event.key)    
                self.shared_dict['current_ship'] = self.current_ship
                
                
    def update(self):
        GameView.update(self)
    
        self.get_selected_item(self.system.planets + self.mobs)
    
    def draw(self, screen):
        GameView.draw(self, screen)
        
        if self.selected_item and self.selected_item.object_type() != 'Ship':
            pygame.draw.line(screen, 'white', self.current_ship.xy, self.selected_item.xy)
            pygame.draw.circle(screen, 'white', self.selected_item.xy, self.selected_item.size+SYSTEM_HIGHLIGHT, SYSTEM_HIGHLIGHT )

        
        pygame.draw.circle(screen, utils.fade_color_to(self.system.color, pygame.Color('black'), 2/3), const.screen_center, (self.system.r+2)*SUN_SIZE_MULT)
        pygame.draw.circle(screen, utils.fade_color_to(self.system.color, pygame.Color('black'), 1/3), const.screen_center, (self.system.r+1)*SUN_SIZE_MULT)
        pygame.draw.circle(screen, self.system.color, const.screen_center, self.system.r*SUN_SIZE_MULT )
        
        for planet in self.system.planets:
            planet.solar_view_draw(screen)
       
        GameView.draw_objects(self, screen)
        
        
    def get_mouse_text(self):
        text = []
        if self.selected_item:
            text.append(self.selected_item.description())
            for mob in self.mobs:
                if mob.planet == self.selected_item:
                    text.append(mob.description())
                    
        return text
    
    
    def get_local_allies(self):
        allies = []
        for ship in self.ships:
            if not ship.is_npc and ship.system == self.current_ship.system:
                allies.append(ship)
        return allies     
    
    
    
    


