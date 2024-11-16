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
SHIP_LAUNCH_TIMER = 50

class GalaxyView(game_view.GameView):
    
    def __init__(self, screen, ships):
        game_view.GameView.__init__(self, screen, ships)
    
        if ships[0].system:
            ships[0].reset_xy(ships[0].system.xy)
        
        self.current_system = None
        self.selected_system = None
        
        self.mobs = [ships[0]]
        
        for ship in self.ships:
            if ship.is_moving():
                self.mobs.append(ship)
        
    def process_inputs(self):
        
        view = self
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if self.current_system and not self.ships[0].is_moving():
                        view = solar_view.SolarView(self.screen, self.current_system, self.ships)
                if  event.key == pygame.K_j:   
                    if self.selected_system and self.ships[0].can_jump(self.selected_system.xy):
                        self.ships[0].destination = self.selected_system.xy

        
        return view
            
    def update(self):

        
        for mob in self.mobs:
            if mob.name == 'Hero' or self.ships[0].is_moving():
                mob.update()
    
    
        self.selected_system = None
        mousepos = Vector2(pygame.mouse.get_pos())
        for system in systems.syslist:
            if system.xy.distance_to(mousepos) < MOUSE_RADIUS:
                self.selected_system = system
            if self.ships[0].xy == system.xy:
                self.current_system = system
        
        if self.ships[0].is_moving():
            self.master_timer += 1
            
        
        if self.master_timer % SHIP_LAUNCH_TIMER == 0:
            suitable = []
            for ship in self.ships:
                if ship.is_npc and ship.species == 'Hostile' and ship.xy != const.home:
                    suitable.append(ship)
            
            suitable.sort(key=lambda x: x.xy.distance_to(const.home))
            
            
            fresh_mob = suitable[0]
            
            
            fresh_mob.destination = const.home
            self.mobs.append(fresh_mob)
            
        for mob in self.mobs:
            if mob.is_npc and not mob.is_moving():
                self.mobs.remove(mob)
                if mob.xy == const.home:
                    self.threat_level += 1
        
        
    def draw(self):
        
        game_view.GameView.draw(self)

        if self.threat_level >= 11:
            text = "Game Over"
            big_font = pygame.font.SysFont('Comic Sans MS', 100)
            text_surface = big_font.render(text, False, 'white', 'black')
            text_width, text_height = text_surface.get_size()
            text_pos = Vector2(const.screen_width / 2 - text_width / 2, const.screen_height / 2 - text_height / 2)
            self.screen.blit(text_surface, text_pos )
            
            pygame.display.flip() 
            pygame.time.wait(10000)
            pygame.quit()
            raise SystemExit
            
        for system in systems.syslist:
            
            pygame.draw.circle(self.screen, utils.fade_to_black(system.color, 2, 3), system.xy, system.r+2)
            pygame.draw.circle(self.screen, utils.fade_to_black(system.color, 1, 3), system.xy, system.r+1)
            pygame.draw.circle(self.screen, system.color, system.xy, system.r )

    
        # draw red halo around home
        pygame.draw.circle(self.screen, 'red', (const.screen_width - const.free_space_in_corners, const.free_space_in_corners), systems.HOME_STAR_SIZE+2, self.threat_level )

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
        
        
        
        
        
        
        
        
        