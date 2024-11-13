#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 17:48:16 2024

@author: steve
"""

import pygame
from pygame.math import Vector2

import game_view
import systems
import utils
import constants as const
import solar_view


MOUSE_RADIUS = 5
TEXT_OFFSET = 15
SYSTEM_HIGHLIGHT = 3

class GalaxyView(game_view.GameView):
    
    def __init__(self, screen, ships):
        game_view.GameView.__init__(self, screen, ships)
    

        ships[0].reset_xy(ships[0].location.galaxy_xy)
        # FIXME: heading too!
        
        self.current_system = systems.syslist[0]    # FIXME
        self.selected_system = None
        
        self.mobs = [ships[0]]
        
        for ship in self.ships:
            if ship.destination != ship.location.galaxy_xy:
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
                if  event.key == pygame.K_j:   
                    if self.selected_system and self.ships[0].can_jump(self.selected_system.xy):
                        self.ships[0].destination = self.selected_system.xy
        """          
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_d]:
            self.ships[0].heading += 10
        if keys[pygame.K_a]:      
            self.ships[0].heading -= 10  
        if keys[pygame.K_w]:
            self.ships[0].xy.y -= 1  
        if keys[pygame.K_x]:
            self.ships[0].xy.y += 1     
        """
        
        return view
            
    def update(self):
        game_view.GameView.update(self)
    
    
        self.selected_system = None
        mousepos = Vector2(pygame.mouse.get_pos())
        for system in systems.syslist:
            if system.xy.distance_to(mousepos) < MOUSE_RADIUS:
                self.selected_system = system
        
    def draw(self):
        
        game_view.GameView.draw(self)

        
        for system in systems.syslist:
            
            pygame.draw.circle(self.screen, utils.fade_to_black(system.color, 2, 3), system.xy, system.r+2)
            pygame.draw.circle(self.screen, utils.fade_to_black(system.color, 1, 3), system.xy, system.r+1)
            pygame.draw.circle(self.screen, system.color, system.xy, system.r )

    
        threat_level = 3
        pygame.draw.circle(self.screen, 'red', (const.screen_width - const.free_space_in_corners, const.free_space_in_corners), systems.HOME_STAR_SIZE+2, threat_level )

        if self.selected_system:
            

            if self.ships[0].can_jump(self.selected_system.xy):
                pygame.draw.line(self.screen, 'white', self.ships[0].xy, self.selected_system.xy)
                pygame.draw.circle(self.screen, 'white', self.selected_system.xy, self.selected_system.r+SYSTEM_HIGHLIGHT, SYSTEM_HIGHLIGHT )

            else:
                distance = self.ships[0].xy.distance_to(self.selected_system.xy)
                ratio = self.ships[0].resources['fuel'] / distance                
                newpoint = self.ships[0].xy.lerp(self.selected_system.xy, ratio)

                pygame.draw.line(self.screen, 'white', self.ships[0].xy, newpoint) 
                pygame.draw.line(self.screen, 'red', newpoint, self.selected_system.xy) 
                
                

            text = self.selected_system.name + ': ' + self.selected_system.system_type
            text_surface = self.font.render(text, True, 'white', 'black')
            
            text_width, text_height = text_surface.get_size()
            text_pos = self.selected_system.xy + (TEXT_OFFSET,TEXT_OFFSET)
            
            if text_width > const.screen_width - text_pos[0]:
                text_pos = self.selected_system.xy + (-text_width - TEXT_OFFSET,TEXT_OFFSET)
            
            if text_height > const.screen_height - text_pos[1]:
                text_pos = self.selected_system.xy + (TEXT_OFFSET, -text_height - TEXT_OFFSET)

            self.screen.blit(text_surface, text_pos )
                
        game_view.GameView.draw_objects(self) 
        
        
        
        
        
        
        
        
        