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

    myship = ships.Ship(hero_name, (const.free_space_in_corners,const.screen_height-const.free_space_in_corners), None, None, False)
    myship.is_current = True



    shiplist = [ myship ]

    for system in systems.syslist:
        if system.system_type != 'Uninhabited' and system != home_system:
            planet = system.planets[my_random.my_randint(0, len(system.planets)-1)]
            shiplist.append(ships.Ship(system.name, system.xy, system, planet, True))
    
    
    for ship in shiplist:
        if ship.name == 'Ainalrami' or ship.name == 'Menkent':
            ship.is_npc = False
            ship.liege = hero_name
    

    def __init__(self):
        self.next_view = None     
        self.font = utils.fonts[20]
        self.ships = GameView.shiplist
        self.current_ship = GameView.myship
        
        self.mobs = []
        self.master_timer = 1
        self.threat_level = 3
        
        self.selected_item = None
        
    def update(self):
        
        for mob in self.mobs:
            mob.update()
        
    def draw(self, screen):
        
        screen.fill('black') 
        
        utils.draw_stars(screen)
        
        self.draw_textbox(screen)
  
    def draw_textbox(self, screen): 
        
        pygame.draw.rect(screen, 'white', [0, const.screen_height , const.screen_width, 2])
        
        resource_str = ''
        for key in self.current_ship.resources.keys():
            resource_str = resource_str + (key.capitalize() + ': {:4.1f}    '.format(self.current_ship.resources[key]))

        text_surface = self.font.render(resource_str, True, 'white')      
        font_height = self.font.size(resource_str)[1]       
        text_offset = (TEXTBOX_HEIGHT - font_height) /2        
        screen.blit(text_surface, (10, const.screen_height+text_offset))

        
    def draw_objects(self, screen):
        
        for mob in self.mobs:
            mob.draw(screen)
        
        # mouseover text
        if self.selected_item:
            
            textbox_width = 0
            textbox_height = 0
            text_arr = self.get_mouse_text()
            for text in text_arr:
                size = self.font.size(text)
                textbox_width = textbox_width if size[0] < textbox_width else size[0]
                textbox_height += size[1]
                
            surface = pygame.Surface((textbox_width, textbox_height))
            
            for i in range(0, len(text_arr)):
                text_surface = self.font.render(text_arr[i], True, 'white', 'black')
                surface.blit(text_surface,  (0, size[1] * (i)))
        
            
            text_pos = self.selected_item.xy + (TEXT_OFFSET,TEXT_OFFSET)


            if textbox_width > const.screen_width - text_pos[0]:
                text_pos = self.selected_item.xy + (-textbox_width - TEXT_OFFSET,TEXT_OFFSET)
            
            if textbox_height > const.screen_height - text_pos[1]:
                text_pos = self.selected_item.xy + (TEXT_OFFSET, -textbox_height - TEXT_OFFSET)
        
            screen.blit(surface, text_pos )
            
    def get_selected_item(self, items):
        self.selected_item = None
        mousepos = Vector2(pygame.mouse.get_pos())
        for item in items:
            if item.xy.distance_to(mousepos) < MOUSE_RADIUS:
                self.selected_item = item
                break
        
    def process_game_event(self, event):
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFTBRACKET or event.key == pygame.K_RIGHTBRACKET:  

                allied_ships = self.get_local_allies()
                index = allied_ships.index(self.current_ship)
                if event.key == pygame.K_LEFTBRACKET:
                    index = (index - 1) % len(allied_ships)
                else:
                    index = (index + 1) % len(allied_ships)   
                
                self.current_ship.is_current = False
                self.current_ship = allied_ships[index]
                self.current_ship.is_current = True

 
class ViewManager():
    
    def __init__(self):
        self.screen = pygame.display.set_mode((const.screen_width, const.screen_height+TEXTBOX_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Return to ' + const.our_capital)
        
        
    def setup_views(self, view_dict, start_view):
        self.view_dict = view_dict
        self.view = self.view_dict[start_view]
        self.view.startup(None)

        
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
                
            self.view.process_game_event(event)
            self.view.process_event(event)
            
    def run(self):
        
        while True:
            self.event_loop()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(24)


    
    
