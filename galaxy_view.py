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

SYSTEM_HIGHLIGHT = 3
SHIP_LAUNCH_TIMER = 50

class GalaxyView(game_view.GameView):
    
    def __init__(self, screen, current_ship, ships):
        game_view.GameView.__init__(self, screen, current_ship, ships)
    
        if self.current_ship.system:
            self.current_ship.reset_xy(self.current_ship.system.xy)
        
        self.current_system = None
        
        for ship in self.ships:
            if ship.is_moving() or not ship.is_npc:
                self.mobs.append(ship)
    
        
    def process_inputs(self):
        
        view = self
        
        for event in pygame.event.get():
            self.process_event(event)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if self.current_system and not self.current_ship.is_moving():
                        view = solar_view.SolarView(self.screen, self.current_system, self.current_ship, self.ships)
                if  event.key == pygame.K_j:   
                    if self.selected_item and self.current_ship.can_jump(self.selected_item.xy):
                        self.current_ship.destination = self.selected_item.xy
                if event.key == pygame.K_LEFTBRACKET or event.key == pygame.K_RIGHTBRACKET:  

                   index = self.myships.index(self.current_ship)
                   if event.key == pygame.K_LEFTBRACKET:
                       index = (index - 1) % len(self.myships)
                   else:
                       index = (index + 1) % len(self.myships)      
                   self.current_ship = self.myships[index]

        
        return view
            
    def update(self):

        
        for mob in self.mobs:
            if not mob.is_npc or self.current_ship.is_moving():
                mob.update()
        
        self.get_selected_item(systems.syslist)

        for system in systems.syslist:
            if self.current_ship.xy == system.xy:
                self.current_system = system
        
        if self.current_ship.is_moving():
            self.master_timer += 1
            
        
        if self.master_timer % SHIP_LAUNCH_TIMER == 0:
            suitable = []
            for ship in self.ships:
                if ship.is_npc and ship.liege == 'Baddies' and ship.xy != const.home:     # FIXME: Baddies 
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

        if self.selected_item:
            

            if self.current_ship.can_jump(self.selected_item.xy):
                pygame.draw.line(self.screen, 'white', self.current_ship.xy, self.selected_item.xy)
                pygame.draw.circle(self.screen, 'white', self.selected_item.xy, self.selected_item.r+SYSTEM_HIGHLIGHT, SYSTEM_HIGHLIGHT )

            else:
                distance = self.current_ship.xy.distance_to(self.selected_item.xy)
                ratio = self.current_ship.resources['fuel'] / distance                
                newpoint = self.current_ship.xy.lerp(self.selected_item.xy, ratio)

                pygame.draw.line(self.screen, 'white', self.current_ship.xy, newpoint) 
                pygame.draw.line(self.screen, 'red', newpoint, self.selected_item.xy) 
                
                
        game_view.GameView.draw_objects(self) 
        
        
    def get_mouse_text(self):
        text = []
        if self.selected_item:
            text.append(self.selected_item.description())
            for mob in self.mobs:
                if mob.system == self.selected_item:
                    text.append(mob.description())
                    
        return text
            
        
        
        
        
        
        