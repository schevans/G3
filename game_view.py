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
import copy
import pickle
from statistics import mean 
import webbrowser
from collections import deque
import math
import json

import ships
import systems
import constants as const
import utils
from exposition import ExpositionBox

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
    

class State(Enum):
    IN_PROGRESS = 1,
    GAME_OVER = 2,
    VICTORY = 3
    

class GameView():
      
    hero_name = 'Hero'      # FIXME: Move to Menu
    
    # FIXME: Move all this?
    utils.init_stars(const.num_stars)       
    systems.init_systems(const.num_systems)
    
    
    home_system = systems.syslist[0]
    home_planet = home_system.planets[0]

    my_ship = ships.Ship(hero_name, const.initial_ship_position, None, None, False, None, True)
    my_ship.is_current = True

    shiplist = [ my_ship ]

    for system in systems.syslist:
        if system.system_type != 'Uninhabited' and system.name != const.our_capital:
            planet = system.planets[my_random.my_randint(0, len(system.planets)-1)]
            if system.name in const.species_color.keys():
                shiplist.append(ships.Ship(system.name, system.xy, system, planet, True, '22222222'))
            else:
                shiplist.append(ships.Ship(system.name, system.xy, system, planet, True))
    
    # dev mode for testing recruits
    if const.dev_mode >= 3:
        for ship in shiplist:
            if ship.liege == const.friendly_capital:
                ship.recruit()
                ship.resources = ship.resources.fromkeys(ship.resources, 999)
                ship.resources['laser'] = math.inf
    
    
    def __init__(self):
        self.next_view = None     
        self.font = utils.fonts[20]
        self.ships = GameView.shiplist
        self.current_ship = GameView.my_ship
        
        self.mobs = []
        
        self.selected_item = None
        
        self.exposition = deque()
        
        self.doubleclick_timer = pygame.time.Clock()
        self.clock_tick = const.clock_tick
        
        self.manual_url = './story/ship_manual.html'
        self.manual_text = 'Ship Manual'
        self.manual_surface_normal = self.font.render(self.manual_text, True, 'white') 
        self.manual_surface_highlight = self.font.render(self.manual_text, True, const.hyperlink_blue) 
        self.manual_surface = self.manual_surface_normal
        manual_width, manual_height = self.font.size(self.manual_text)     
        self.manual_pos = (const.screen_width - manual_width-5, const.screen_height-manual_height)
        self.manual_rect = pygame.Rect((const.screen_width - manual_width-5, const.screen_height-manual_height), (manual_width+10, manual_height))


    def process_event(self, event):
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if len(self.shared_dict['history']):
                    if self.shared_dict['history'][-1] in [View.FITTING, View.LOAD_SAVE, View.DOCKING]:
                        self.shared_dict['history'].pop()
                        self.next_view = (self.shared_dict['history'].pop(), self.shared_dict)
            if event.key == pygame.K_f:
                self.next_view = (View.FITTING, self.shared_dict)
            if event.key == pygame.K_LEFTBRACKET or event.key == pygame.K_RIGHTBRACKET:  
                self.current_ship = self.do_ship_swap(event.key)
                self.shared_dict['current_ship'] = self.current_ship
            if event.key == pygame.K_l:
                self.next_view = (View.LOAD_SAVE, self.shared_dict)
                
        if self.exposition and (not self.exposition[0].is_help or self.shared_dict['show_help']):
           self.exposition[0].process_event(event)
           
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.manual_rect.collidepoint(pygame.mouse.get_pos()):
                webbrowser.open(self.manual_url)
          
            
    def update(self):
        
        for mob in self.mobs:
            mob.update()
            
        if self.exposition and (not self.exposition[0].is_help or self.shared_dict['show_help']):
            self.exposition[0].update()
            
        if self.manual_rect.collidepoint(pygame.mouse.get_pos()):
            self.manual_surface = self.manual_surface_highlight
        else:
            self.manual_surface = self.manual_surface_normal
            
        
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

        pygame.draw.rect(screen, 'black', self.manual_rect)
        screen.blit(self.manual_surface, self.manual_pos)
        

    def draw_objects(self, screen):
        
        for mob in self.mobs:
            mob.draw(screen)
        
        # mouseover text
        if self.selected_item:
            self.draw_mouseover_text(screen, self.get_mouse_text())
               
        if self.exposition and (not self.exposition[0].is_help or self.shared_dict['show_help']):
            self.exposition[0].draw(screen)


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
        self.exposition.popleft()
    
    def exposition_checkbox_callback(self, is_checked):
        self.shared_dict['show_help'] = is_checked
 
    def draw_game_state(self, screen):
        if self.shared_dict['game_state'] != State.IN_PROGRESS:
            text = self.shared_dict['game_state'].name.replace('_', ' ') +'!'
            text_surface = utils.fonts[100].render(text, False, 'white', 'black')
            text_width, text_height = text_surface.get_size()
            text_pos = Vector2(const.screen_width / 2 - text_width / 2, const.screen_height / 2 - text_height / 2)
            screen.blit(text_surface, text_pos )   
            
            if self.shared_dict['game_state'] == State.VICTORY:
                self.victory_dump()
                
    
    def victory_dump(self):
        
        with open('./data/VictoryDump' + str(const.random_seed) + '.json', 'w') as f:
            
            data = []
            data.append(self.shared_dict['master_timer']())
            
            is_dead = []
            ship_data = {}
            for ship in self.ships:
                if ship.is_alive:
                    if not ship.is_npc:
                        ship_data[ship.name] = {}
                        ship_data[ship.name]['resources'] = ship.resources
                        ship_data[ship.name]['fit'] = ship.fit.to_string()
                else:
                    is_dead.append(ship.name + ' (' + ship.liege + ')')
            
            data.append(ship_data)
            data.append(is_dead)
            
            json.dump(data, f, indent=4)
            f.close()
        
 
    def pickle(self):
        
        data = copy.copy(self.shared_dict)
        data['current_ship'] = data['current_ship'].name
        data['system'] = data['system'].name if data['system'] else None
        data['planet'] = data['planet'].name if data['planet'] else None
        data['other_ship'] = data['other_ship'].name if data['other_ship'] else None
        data['fogofwar_mask'] = None # saved separately as a png for smaller save files
            
        return data
    
    
    def unpickle(self, data, fogofwar_mask):
        
        self.shared_dict = data
        
        self.shared_dict['current_ship'] = next(x for x in self.ships if x.name == self.shared_dict['current_ship'])
        self.shared_dict['system'] = next((x for x in systems.syslist if x.name == self.shared_dict['system']), None)
        if self.shared_dict['system'] and self.shared_dict['planet']:
            self.shared_dict['planet'] = next(x for x in self.shared_dict['system'].planets if x.name == self.shared_dict['planet'])
        
        # handle saving during docking view for completeness
        if self.shared_dict['system'] and self.shared_dict['planet'] and self.shared_dict['other_ship']:
            other_ship = next((x for x in self.ships if x.name == self.shared_dict['other_ship']), None)
            if not other_ship:
                other_ship = self.shared_dict['planet'].station
            self.shared_dict['other_ship'] = other_ship
        
        self.shared_dict['fogofwar_mask'] = fogofwar_mask
        
        
    def save_game(self, filename):

        ships = [x.pickle() for x in self.ships]
        
        data = [self.pickle(), ships, systems.pickle(), my_random.get_state()]

        with open(filename, "wb") as f:
            pickle.dump(data, f)
            f.close()

        pygame.image.save(self.shared_dict['fogofwar_mask'], filename.replace('pkl', 'png'))

    def load_game(self, filename):
    
        with open(filename, "rb") as f:
            data = pickle.load(f)
            f.close()
            
        fogofwar_mask = pygame.image.load(filename.replace('pkl', 'png'))
        
        self.unpickle(data[0], fogofwar_mask)
        
        for i in range(len(data[1])):
            self.ships[i].unpickle(systems.syslist, data[1][i])

        systems.unpickle(data[2])  
        
        my_random.set_state(data[3])
        
    
    def show_exposition(self, expo_enum):
        
        if expo_enum not in self.shared_dict['expositions_done']:
            self.exposition.append(ExpositionBox(expo_enum, self.exposition_ok_callback, self.exposition_checkbox_callback))
            self.shared_dict['expositions_done'].append(expo_enum)
            
            
class ViewManager():
    
    def __init__(self):
        self.screen = pygame.display.set_mode((const.screen_width, const.screen_height+TEXTBOX_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Return to ' + const.our_capital)
        
        
    def setup_views(self, view_dict, start_view):
        self.view_dict = view_dict
        self.view = self.view_dict[start_view]
        
        fogofwar_mask = pygame.image.load('./data/FogOfWarStart.png')
        
        shared_dict = {
            'current_ship': GameView.my_ship,
            'system': None,
            'planet': None,
            'history': [],
            'master_timer': MasterTimer(0),
            'other_ship': None,
            'fogofwar_mask': fogofwar_mask,
            'show_help': const.exposition_on,
            'expositions_done': [],
            'game_state': State.IN_PROGRESS,
            'threat_level': const.threat_level_start
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
            self.clock.tick(self.view.clock_tick)
            
    def solve(self):
         
        self.system_resources = {}
        
        for system in systems.syslist:
            self.system_resources[system] = const.our_initial_resources.fromkeys(const.our_initial_resources, 0)
            for planet in system.planets:
                for key in planet.resources:
                    self.system_resources[system][key] += planet.resources[key]

        ship = copy.copy(GameView.shiplist[0])

        route = []
        num_branches = [0,0,[],[]]

        self.jump_solve(ship, route, num_branches)

        lengths = [len(i) for i in num_branches[2]]
        average = 0 if len(lengths) == 0 else (float(sum(lengths)) / len(lengths)) 
        
        print(num_branches[0], 'paths,', num_branches[1], 'home,', round(num_branches[1]/num_branches[0]*100, 2), '%,', round(average, 2), 'av#jumps')
        
        mean_resources = {}     
        for key in const.our_initial_resources.keys():
            mean_resources[key] = mean([d[key] for d in num_branches[3]])
        
        print(mean_resources)
                
    def jump_solve(self, ship, route, num_branches):
        
        num_branches[0] += 1
        
        for system in systems.syslist:
            
            if ship.can_jump(system) and system.xy[0] > ship.xy[0] and system.xy[1] < ship.xy[1]: 
                if system.name == 'Polaris':
                    num_branches[1] += 1
                    num_branches[2].append(route)                    
                    num_branches[3].append(ship.resources)
                    break
                
                newship = copy.copy(ship)
                newship.resources = ship.resources.copy()
                newship.resources['fuel'] -= ship.jump_cost(system)
                newship.reset_xy(system.xy)
                
                for key in self.system_resources[system]:
                    newship.resources[key] +=self.system_resources[system][key]
                    
                newroute = route.copy()
                newroute.append(system.name)
                self.jump_solve(newship, newroute, num_branches )

        
class MasterTimer():

    def __init__(self, weeks):
        self.weeks = weeks

    def __call__(self):
        return self.weeks

    def increment(self):
        self.weeks += 1        

            








    
    
