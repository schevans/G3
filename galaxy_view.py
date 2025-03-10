#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 17:48:16 2024

@author: steve
"""

import pygame
from pygame.math import Vector2


import systems
import utils
import constants as const



from game_view import GameView, View

  
SYSTEM_HIGHLIGHT = 3
SHIP_LAUNCH_TIMER = 50   
class GalaxyView(GameView):
    
    def __init__(self):
        GameView.__init__(self) 
        
    def cleanup(self):
        self.mobs = []
        
    def startup(self, shared_dict):
        self.shared_dict = shared_dict
        self.shared_dict['history'].append(View.GALAXY)
        self.current_ship = self.shared_dict['current_ship']
          
        for ship in self.ships:
            if ship.is_moving() or not ship.is_npc:
                self.mobs.append(ship)
                if self.current_ship.system and ship.system == self.current_ship.system:
                    ship.reset_xy(ship.system.xy)

        self.is_waiting = False
        
    def process_event(self, event):
        
        GameView.process_event(self, event)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                if self.current_ship.system and not self.current_ship.is_moving():
                    self.shared_dict['system'] = self.current_ship.system
                    self.next_view = (View.SOLAR, self.shared_dict)
            if event.key == pygame.K_j:   
                if self.selected_item and self.current_ship.can_jump(self.selected_item.xy):
                    self.current_ship.destination = self.selected_item
            if event.key == pygame.K_w:
                self.shared_dict['other_ship'] = GameView.shiplist[8]       # FIXME: Temp
                self.next_view = (View.DOCKING, self.shared_dict)
            if event.key == pygame.K_q: # TEMP
                self.current_ship.planet = GameView.TEMP_PLANET
                self.current_ship.system = GameView.TEMP_SYSTEM
                self.shared_dict['planet'] = GameView.TEMP_PLANET
                self.next_view = (View.PLANET, self.shared_dict)

                    
        keys = pygame.key.get_pressed() 
        self.is_waiting = False
        if keys[pygame.K_z]:
            self.is_waiting = True  
                
    def update(self):
        
        if self.exposition:
            self.exposition.update()
        
        for mob in self.mobs:
            if self.my_ship.is_moving() or self.is_waiting:
                mob.update()
        
        self.get_selected_item(systems.syslist + self.mobs)
        
        if self.current_ship == self.my_ship and ( self.current_ship.is_moving() or self.is_waiting):
            self.master_timer += 1
            
        
        if self.master_timer % SHIP_LAUNCH_TIMER == 0:
            self.master_timer += 1
            
            suitable = []
            for ship in self.ships:
                if ship.is_npc and ship.liege == const.hostile_capital and ship.xy != const.home_xy:
                    suitable.append(ship)
            
            suitable.sort(key=lambda x: x.xy.distance_to(const.home_xy))
            
            fresh_mob = suitable[0]

            fresh_mob.destination = self.home_system
            self.mobs.append(fresh_mob)
            
            
        for mob in self.mobs:
            if mob.is_npc and not mob.is_moving():
                self.mobs.remove(mob)
                if mob.xy == const.home_xy:
                    self.threat_level += 1
    
    def draw(self, screen):
        
        GameView.draw(self, screen)
            
        for system in systems.syslist:
            
            pygame.draw.circle(screen, utils.fade_color_to(system.color, pygame.Color('black'), 2/3), system.xy, system.r+2)
            pygame.draw.circle(screen, utils.fade_color_to(system.color, pygame.Color('black'), 1/3), system.xy, system.r+1)
            pygame.draw.circle(screen, system.color, system.xy, system.r )

    
        text = 'Days passed: ' + str(self.master_timer)
        text_surface = utils.fonts[20].render(text, True, 'white', 'black')
        screen.blit(text_surface, (15, 15) )
        
        # draw red halo around home
        pygame.draw.circle(screen, 'red', (const.screen_width - const.free_space_in_corners, const.free_space_in_corners), systems.HOME_STAR_SIZE+2, self.threat_level )

        if self.threat_level >= 11:
            text = "Game Over"
            text_surface = utils.fonts[100].render(text, False, 'white', 'black')
            text_width, text_height = text_surface.get_size()
            text_pos = Vector2(const.screen_width / 2 - text_width / 2, const.screen_height / 2 - text_height / 2)
            screen.blit(text_surface, text_pos )


        if self.selected_item and self.selected_item.object_type() != 'Ship':
            

            if self.current_ship.can_jump(self.selected_item.xy):
                pygame.draw.line(screen, 'white', self.current_ship.xy, self.selected_item.xy)
                pygame.draw.circle(screen, 'white', self.selected_item.xy, self.selected_item.r+SYSTEM_HIGHLIGHT, SYSTEM_HIGHLIGHT )

            else:
                distance = self.current_ship.xy.distance_to(self.selected_item.xy)
                ratio = self.current_ship.resources['fuel'] / distance                
                newpoint = self.current_ship.xy.lerp(self.selected_item.xy, ratio)

                pygame.draw.line(screen, 'white', self.current_ship.xy, newpoint) 
                pygame.draw.line(screen, 'red', newpoint, self.selected_item.xy) 
                
                
        GameView.draw_objects(self, screen) 
        
    def get_mouse_text(self):
        text = []
        if self.selected_item:
            text.append(self.selected_item.description())
            for mob in self.mobs:
                if mob.system == self.selected_item:
                    text.append(mob.description())
                    
        return text
        
    def get_local_allies(self):
        allies = []
        for ship in self.ships:
            if not ship.is_npc:
                allies.append(ship)
        return allies        
        