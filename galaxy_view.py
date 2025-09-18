#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 17:48:16 2024

@author: steve
"""

import pygame

import systems
import utils
import constants as const
from game_view import GameView, View, State
from exposition import ExpositionText

SYSTEM_HIGHLIGHT = 3
SHIP_LAUNCH_TIMER = 50   
OPENING_TIMER = 50

FOW_ENEMY_HALO = 20

class GalaxyView(GameView):
    
    def __init__(self):
        GameView.__init__(self) 
        self.opening_timer = 0
        
    def cleanup(self):
        self.mobs = []
        
    def startup(self, shared_dict):
        self.shared_dict = shared_dict
        self.shared_dict['history'] = [(View.GALAXY)]
        self.current_ship = self.shared_dict['current_ship']
        self.master_timer = self.shared_dict['master_timer']
        self.fogofwar_mask = self.shared_dict['fogofwar_mask']
        
        for ship in self.ships:
            if ship.is_alive and ship.is_moving() or not ship.is_npc:
                self.mobs.append(ship)
                if self.current_ship.system and ship.system == self.current_ship.system:
                    ship.reset_xy(ship.system.xy)

        self.is_waiting = False
        
    def process_event(self, event):
        
        GameView.process_event(self, event)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.current_ship.system and not self.current_ship.is_moving():
                    self.shared_dict['system'] = self.current_ship.system
                    self.next_view = (View.SOLAR, self.shared_dict)
                    
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == const.left_mouse_click:
            if self.doubleclick_timer.tick() < const.doubleclick_delay:
                if self.selected_item and self.current_ship.can_jump(self.selected_item.xy):
                    self.current_ship.resources['fuel'] -= self.current_ship.jump_cost(self.selected_item.xy)
                    self.current_ship.destination = self.selected_item
            
        keys = pygame.key.get_pressed() 
        self.is_waiting = False
        if keys[pygame.K_z] and not self.flagship.is_moving():
            self.is_waiting = True  
                
    def update(self):
        
        # this doesn't call GameView.update as it does it's own thing with mob.update
        if self.shared_dict['show_help'] and self.exposition:
            self.exposition[0].update()
        
        mousepos = pygame.mouse.get_pos()
        if self.manual_rect.collidepoint(mousepos):
            self.manual_surface = self.manual_surface_highlight
        else:
            self.manual_surface = self.manual_surface_normal
        
        for mob in self.mobs:
            if self.my_ship.is_moving() or self.is_waiting:
                mob.update()
                
                fow_halo = FOW_ENEMY_HALO if mob.is_npc else mob.fit.systems['scanner'].value
                pygame.draw.circle(self.fogofwar_mask, (0,0,0,0), mob.xy, fow_halo)
                
            if mob == self.current_ship:    # ship may have upgraded scanner
                pygame.draw.circle(self.fogofwar_mask, (0,0,0,0), mob.xy, mob.fit.systems['scanner'].value)
         
        self.selected_item = None
        if self.fogofwar_mask.get_rect().collidepoint(mousepos) and self.fogofwar_mask.get_at(mousepos) != const.fogofwar_black:
            self.get_selected_item(systems.syslist + self.mobs)
        
        if self.flagship.is_moving() or self.is_waiting:
            self.master_timer.increment()
            
        if self.opening_timer <= OPENING_TIMER:
            if self.opening_timer == OPENING_TIMER and not const.dev_mode:
                self.show_exposition(ExpositionText.OPENING)
            self.opening_timer += 1
        
        if self.master_timer() % SHIP_LAUNCH_TIMER == 0 and self.master_timer() != 0:
            self.master_timer.increment()
            
            suitable = []
            for ship in self.ships:
                if ship.is_npc and ship.liege == const.hostile_capital and ship.xy != const.home_xy:
                    suitable.append(ship)
            
            suitable.sort(key=lambda x: x.xy.distance_to(const.home_xy))
            
            fresh_mob = suitable[0]

            fresh_mob.destination = self.home_system
            fresh_mob.system = None
            fresh_mob.planet = None
            self.mobs.append(fresh_mob)
            self.show_exposition(ExpositionText.FIRST_ENEMY_LAUNCH)
            
        if self.shared_dict['show_help'] and ExpositionText.FIRST_SYSTEM not in self.shared_dict['expositions_done']:
            if not self.current_ship.is_moving() and self.current_ship.destination and self.current_ship.destination.object_type() == 'System':
                self.show_exposition(ExpositionText.FIRST_SYSTEM)
            
        for mob in self.mobs:
            if mob.is_npc and not mob.is_moving():
                self.mobs.remove(mob)
                if mob.xy == const.home_xy:
                    mob.system = GameView.home_system
                    mob.planet = GameView.home_planet
                    self.threat_level += 1
                    self.show_exposition(ExpositionText.FIRST_ENEMY_LAND)
    
    def draw(self, screen):
        
        GameView.draw(self, screen)
            
        for system in systems.syslist:          
            pygame.draw.circle(screen, utils.fade_color_to(system.color, pygame.Color('black'), 2/3), system.xy, system.star.size+2)
            pygame.draw.circle(screen, utils.fade_color_to(system.color, pygame.Color('black'), 1/3), system.xy, system.star.size+1)
            pygame.draw.circle(screen, system.color, system.xy, system.star.size )
        
        # draw red halo around home
        pygame.draw.circle(screen, 'red', (const.screen_width - const.free_space_in_corners, const.free_space_in_corners), systems.HOME_STAR_SIZE+2, self.threat_level )

        if self.threat_level >= 11:
            self.shared_dict['game_state'] = State.GAME_OVER

        if self.selected_item and self.selected_item.object_type() != 'Ship':
            
            if self.current_ship.can_jump(self.selected_item.xy):
                pygame.draw.line(screen, 'white', self.current_ship.xy, self.selected_item.xy)
                pygame.draw.circle(screen, 'white', self.selected_item.xy, self.selected_item.star.size+SYSTEM_HIGHLIGHT, SYSTEM_HIGHLIGHT )

            else:
                jump_cost = self.current_ship.jump_cost(self.selected_item.xy)
                ratio = self.current_ship.resources['fuel'] / jump_cost                
                newpoint = self.current_ship.xy.lerp(self.selected_item.xy, ratio)

                pygame.draw.line(screen, 'white', self.current_ship.xy, newpoint) 
                pygame.draw.line(screen, 'red', newpoint, self.selected_item.xy) 
                
        screen.blit(self.fogofwar_mask, (0, 0))
        
        text = 'Days passed: ' + str(self.master_timer())
        text_surface = utils.fonts[20].render(text, True, 'white', 'black')
        screen.blit(text_surface, (15, 15) )
        
        GameView.draw_objects(self, screen) 

        
    def get_mouse_text(self):
        text = []
        if self.selected_item:
            planets_text = ''
            if self.selected_item.object_type() == 'System':
                if self.current_ship.scanner_lvl() >= const.ScanTarget.NUM_PLANETS:
                    num_planets = len(self.selected_item.planets) 
                    if num_planets > 1:
                        planets_text = ', ' + str(num_planets) + ' planets'
                    else:
                        planets_text = ', ' + str(num_planets) + ' planet'
                
            text.append(self.selected_item.description(self.current_ship.scanner_lvl()) + planets_text)
            for mob in self.mobs:
                if mob.system == self.selected_item:
                    text.append(mob.description(self.current_ship.scanner_lvl()))
                    
        return text
        
    def get_local_allies(self):
        allies = []
        for ship in self.ships:
            if not ship.is_npc:
                allies.append(ship)
        return allies        
        