#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 18:55:32 2024

@author: steve
"""

import pygame
from pygame.math import Vector2
from enum import Enum
import my_random

import ships
import systems
import constants as const
import utils
from exposition import ExpositionBox, ExpositionText

TEXT_OFFSET = 15
MOUSE_RADIUS = 10
TEXTBOX_HEIGHT = 40


class View(Enum):
    MENU = 1
    GALAXY = 2
    SOLAR = 3
    PLANET = 4
    FITTING = 5
    DOCKING = 6
    KEY_BINDINGS = 7
    LOAD_SAVE = 8
    SHIP_SELECT = 9
    GAME_OVER = 10
    CREDITS = 11

class GameView():
      
    hero_name = 'Hero'      # FIXME: Move to Menu
    
    # FIXME: Move all this?
    utils.init_stars(const.num_stars)       
    systems.init_systems(const.num_systems)
    
    
    home_system = systems.syslist[0]

    my_ship = ships.Ship(hero_name, (const.free_space_in_corners,const.screen_height-const.free_space_in_corners), None, None, False)
    my_ship.is_current = True



    shiplist = [ my_ship ]

    for system in systems.syslist:
        if system.system_type != 'Uninhabited' and system.name != const.our_capital:
            planet = system.planets[my_random.my_randint(0, len(system.planets)-1)]
            if system.name in const.species_color.keys():
                shiplist.append(ships.Ship(system.name, system.xy, system, planet, True, '2222222'))
            else:
                shiplist.append(ships.Ship(system.name, system.xy, system, planet, True))
    
    ### TEMP TEMP ###
    TEMP_PLANET = None
    TEMP_SYSTEM = None
    for ship in shiplist:
        if ship.name == 'Fulu':
            ship.is_npc = False
            ship.liege = hero_name
        if ship.name == 'Rigel':
            TEMP_PLANET = ship.planet
            TEMP_SYSTEM = ship.system
    for ship in shiplist:
        if ship.name == 'Fulu':
            ship.planet = TEMP_PLANET
            ship.system = TEMP_SYSTEM    
       
    TEMP_STATION = None
    for system in systems.syslist:
        if system.name == 'Ginan':
            for planet in system.planets:
                if planet.station:
                    TEMP_STATION = planet.station
        
            
    ### TEMP TEMP ###

    def __init__(self):
        self.next_view = None     
        self.font = utils.fonts[20]
        self.ships = GameView.shiplist
        self.current_ship = GameView.my_ship
        
        self.mobs = []
        self.master_timer = 1
        self.threat_level = 3
        
        self.selected_item = None
        
        self.show_help = True
        self.exposition = None 
        self.tmp_ex = 0      # FIXME: Remove
        
    def process_event(self, event):
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x and self.show_help:  # FIXME: Remove
                self.exposition = ExpositionBox(list(ExpositionText)[self.tmp_ex], self.exposition_ok_callback, self.exposition_checkbox_callback)
                self.tmp_ex += 1
                
            if event.key == pygame.K_b:
                if self.shared_dict['history']:
                    self.shared_dict['history'].pop()   # clear the one we're leaving
                    self.next_view = (self.shared_dict['history'].pop(), self.shared_dict)
            if event.key == pygame.K_f:
                self.next_view = (View.FITTING, self.shared_dict)
            if event.key == pygame.K_LEFTBRACKET or event.key == pygame.K_RIGHTBRACKET:  
                self.current_ship = self.do_ship_swap(event.key)
                self.shared_dict['current_ship'] = self.current_ship
                        
        if self.show_help and self.exposition:
           self.exposition.process_event(event)
          
            
    def update(self):
        
        for mob in self.mobs:
            mob.update()
            
        if self.show_help and self.exposition:
            self.exposition.update()
        
    def draw(self, screen):
        
        screen.fill('black') 
        
        utils.draw_stars(screen)
        
        self.draw_textbox(screen)
  
    def draw_textbox(self, screen): 
        
        pygame.draw.rect(screen, 'white', [0, const.screen_height , const.screen_width, 2])
        
        resource_str = ''
        for key in self.current_ship.resources.keys():
            if key != 'laser':
                resource_str = resource_str + (key.capitalize() + ': {:3d}    '.format(int(self.current_ship.resources[key])))
            
        text_surface = self.font.render(resource_str, True, 'white')      
        font_height = self.font.size(resource_str)[1]       
        text_offset = (TEXTBOX_HEIGHT - font_height) /2        
        screen.blit(text_surface, (10, const.screen_height+text_offset))

        
    def draw_objects(self, screen):
        
        for mob in self.mobs:
            mob.draw(screen)
        
        # mouseover text
        if self.selected_item:
            self.draw_mouseover_text(screen, self.get_mouse_text())
            
            
        if self.show_help and self.exposition:
            self.exposition.draw(screen)


    def draw_mouseover_text(self, screen, text_arr):
        
        mousepos = pygame.mouse.get_pos()

        textbox_width = 0
        textbox_height = 0
        for text in text_arr:
            size = self.font.size(text)
            textbox_width = textbox_width if size[0] < textbox_width else size[0]
            textbox_height += size[1]
            
        surface = pygame.Surface((textbox_width, textbox_height))
        
        for i in range(0, len(text_arr)):
            text_surface = self.font.render(text_arr[i], True, 'white', 'black')
            surface.blit(text_surface,  (0, size[1] * (i)))
    
        
        text_pos = Vector2(mousepos) + (TEXT_OFFSET,TEXT_OFFSET)
    
    
        if textbox_width > const.screen_width - text_pos[0]:
            text_pos = mousepos + Vector2(-textbox_width - TEXT_OFFSET,TEXT_OFFSET)
        
        if textbox_height > const.screen_height - text_pos[1]:
            text_pos = mousepos + Vector2(TEXT_OFFSET, -textbox_height - TEXT_OFFSET)
    
        screen.blit(surface, text_pos )

            
    def get_selected_item(self, items):
        self.selected_item = None
        mousepos = Vector2(pygame.mouse.get_pos())
        for item in items:
            if item.xy.distance_to(mousepos) < MOUSE_RADIUS:
                if not item.object_type() in ['Bullet', 'Explosion']: 
                    self.selected_item = item
                    break
        
    def do_ship_swap(self, event_key):
        

        allied_ships = self.get_local_allies()
        index = allied_ships.index(self.current_ship)
        if event_key == pygame.K_LEFTBRACKET:
            index = (index - 1) % len(allied_ships)
        else:
            index = (index + 1) % len(allied_ships)   
        
        self.current_ship.is_current = False
        self.current_ship = allied_ships[index]
        self.current_ship.is_current = True
        
        return self.current_ship
    
    def get_local_allies(self):
        return [self.current_ship]
    
    def exposition_ok_callback(self, button):
        self.exposition = None
    
    def exposition_checkbox_callback(self, is_checked):
        self.show_help = is_checked
 
class ViewManager():
    
    def __init__(self):
        self.screen = pygame.display.set_mode((const.screen_width, const.screen_height+TEXTBOX_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Return to ' + const.our_capital)
        
        
    def setup_views(self, view_dict, start_view):
        self.view_dict = view_dict
        self.view = self.view_dict[start_view]
        
        shared_dict = {
            'current_ship': GameView.my_ship,
            'system': None,
            'planet': None,
            'history': []
            }
        
        self.view.startup(shared_dict)

        
    def update(self):
            
        if self.view.next_view:
            view_name = self.view.next_view[0]
            view_body = self.view.next_view[1]
            self.view.cleanup()
            self.view = self.view_dict[view_name]
            self.view.startup(view_body)
            self.view.next_view = None
            
        self.view.update()
        
    def draw(self):
        self.view.draw(self.screen)
        
    def event_loop(self):
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
                
            self.view.process_event(event)
            
    def run(self):
        
        while True:
            self.event_loop()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(24)


    
    
