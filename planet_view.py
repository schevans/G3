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
from orbital_ships import OrbitalShip
import utils
import my_random
from game_view import GameView, View, State
from explosions import Explosion, LootBox
from exposition import ExpositionText


DOCK_RADIUS = 15

OFFSET = 5
WEAPON_ICON_SIZE = (44, 52)
RESOURCE_BAR = 5
RED_FADE = pygame.Color(207, 1, 0, 64)

class PlanetView(GameView):

    def __init__(self):
        GameView.__init__(self)
        
        
    def cleanup(self):
        self.mobs = []
        self.shared_dict['current_ship'] = self.current_ship.tmpship

    def startup(self, shared_dict):
        self.shared_dict = shared_dict
        self.shared_dict['history'] = [(View.PLANET)]
        
        self.planet = shared_dict['planet']
        
        self.max_resource_rect = pygame.Rect((OFFSET, WEAPON_ICON_SIZE[1] + OFFSET*2), (sum(self.planet.resources.values()) * RESOURCE_BAR, RESOURCE_BAR ))
        
        angle_radians = 0
        
        applicable_mobs = []

        
        for ship in self.ships:
            if ship.planet == self.planet:
                applicable_mobs.append(ship)
           
        self.is_paused = False 
        
        if applicable_mobs:
            angle_increment = ( math.pi * 2 ) / len(applicable_mobs)
            
            for mob in applicable_mobs:                                 
                angle_radians += angle_increment
                orbital_ship = OrbitalShip(mob, self.planet, utils.get_random_r(self.planet.planet_view_r, const.ship_width, self.mobs), angle_radians)

                self.mobs.append(orbital_ship)
                if orbital_ship.tmpship == shared_dict['current_ship']:
                    self.current_ship = orbital_ship
                    
                if mob.liege == const.hostile_capital:
                    self.show_exposition(ExpositionText.FIRST_COMBAT)
                    self.is_paused = True
        
        if self.planet:
            self.show_exposition(ExpositionText.FIRST_PLANET)
        
        
        if self.planet.station:
            self.mobs.append(self.planet.station)
            self.show_exposition(ExpositionText.FIRST_SISTERS)


    def process_event(self, event):
        
        GameView.process_event(self, event)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.shared_dict['system'] = self.planet.system
                self.next_view = (View.SOLAR, self.shared_dict)
            if event.key == pygame.K_SPACE:
                self.is_paused = not self.is_paused
            if event.key == pygame.K_w:
                for mob in self.mobs:
                    if mob.object_type() in ['Ship', 'Station'] and mob.name != 'Hero' and self.current_ship.xy.distance_to(mob.xy) < DOCK_RADIUS:
                        if mob.object_type() == 'Ship': 
                            self.shared_dict['other_ship'] = mob.tmpship
                        else:   # station
                            self.shared_dict['other_ship'] = mob
                        self.next_view = (View.DOCKING, self.shared_dict)
            if pygame.key.name(event.key) in ['1', '2', '3', '4', '5']:
                self.current_ship.weapons.select_from_key(pygame.key.name(event.key))
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == const.right_mouse_click:
        #if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSLASH:        
            self.current_ship.lock_target(pygame.mouse.get_pos(), self.mobs)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == const.left_mouse_click:
        #if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            bullet = self.current_ship.shoot()
            if bullet:
                self.mobs.append(bullet)
                        
        keys = pygame.key.get_pressed() 
        self.current_ship.acceleration = 0
        if keys[pygame.K_d]:
            self.current_ship.acceleration  = const.acc_over_speed * self.current_ship.fit.speed()
        if keys[pygame.K_a]:        
            self.current_ship.acceleration  = -const.acc_over_speed * self.current_ship.fit.speed()
        
        self.clock_tick = const.clock_tick
        if keys[pygame.K_z]:
            self.clock_tick = const.clock_tick * 3
            
              
    def update(self):
        if not self.is_paused:
            GameView.update(self) 
        elif self.shared_dict['show_help'] and self.exposition:
                self.exposition.update()
 
        self.get_selected_item(self.mobs)
        
        self.planet.update()
        
        for mob in self.mobs:
            if mob.object_type() == 'Ship':
                
                bullet = mob.do_ai(self.mobs)
                if bullet:
                   self.mobs.append(bullet)
                   
                mob.check_lock()
                    
                # has been hit by bullet?
                for bullet in (x for x in self.mobs if x.object_type() == 'Bullet' and not x.homing):
                    if bullet.xy.distance_to(mob.xy) <= const.weapon_hit_radius:
                        bullet.hit(mob)
                        
                # has picked up lootbox?
                for lootbox in (x for x in self.mobs if x.object_type() == 'LootBox'):
                    if lootbox.xy.distance_to(mob.xy) <= const.weapon_hit_radius:
                        mob.loot(lootbox)
                        
                # has ship hit planet?      
                if mob.r <= self.planet.planet_view_r + mob.image.width:
                    mob.hit(3,3)
                    mob.r += 5  # and bounce
                        
            # has bullet hit planet => mining
            elif mob.object_type() == 'Bullet' and mob.is_alive:
                if mob.xy.distance_to(const.screen_center) <= self.planet.planet_view_r:
                    resources = self.planet.mine(mob)
                    mob.is_alive = False
                    if resources:
                        r = self.planet.planet_view_r * 4
                        p = my_random.my_random() * ( math.pi * 2 ) 
                        xy = Vector2(const.screen_center.x - math.cos(p)*r,  const.screen_center.y - math.sin(p)*r)
                        self.mobs.append(LootBox(xy, resources))

            # remove the dead things
            if not mob.is_alive:
                self.mobs.remove(mob)
                
                if mob.object_type() == 'Ship':
                    loot_fairy = my_random.my_random()
                    for resource in mob.resources:
                        if resource != 'laser':
                            mob.resources[resource] += int(mob.resources[resource] * loot_fairy)
                    self.mobs.append(Explosion(mob.xy, 30, 1, mob.resources))
                    self.ships.remove(mob.tmpship)
                    if mob.name == 'Hero':      # FIXME hardcode
                        self.game_state = State.GAME_OVER
                elif mob.object_type() == 'Explosion':
                    self.mobs.append(LootBox(mob.xy, mob.resources))
                
        
        if self.home_planet == self.planet and not len(list(mob for mob in self.mobs if mob.object_type() == 'Ship' and mob.is_npc)):
            self.game_state = State.VICTORY
            

    def draw(self, screen):
        
        GameView.draw(self, screen)
        
        self.draw_resource_bar(screen)
        self.current_ship.weapons.draw_icons(screen,self.current_ship.resources, WEAPON_ICON_SIZE, OFFSET)
        self.draw_tooltips(screen)
        
        self.planet.planet_view_draw(screen)
        
        for mob in self.mobs:
            if mob.object_type() == 'Ship' and mob.locked_target:
                pygame.draw.circle(screen, RED_FADE, mob.locked_target.xy, 20, 1)
                pygame.draw.line(screen, RED_FADE, mob.xy, mob.locked_target.xy)
        
        GameView.draw_objects(self, screen)
        
        if self.is_paused:
            text = '[ Paused ]'
            text_surface = utils.fonts[30].render(text, True, 'white', 'black')
            text_width, text_height = text_surface.get_size()
            text_pos = Vector2(const.screen_width / 2 - text_width / 2, text_height + 10)
            screen.blit(text_surface, text_pos )
          
           
          
    def draw_tooltips(self, screen):
        
        tooltip = []
        mousepos = pygame.mouse.get_pos()

        greater_icon_rect = pygame.Rect(((OFFSET,OFFSET), (WEAPON_ICON_SIZE[0]*5+OFFSET*4, WEAPON_ICON_SIZE[1]+OFFSET)))
        
        if greater_icon_rect.collidepoint(mousepos):
            
            start_x = OFFSET
            end_x = OFFSET + WEAPON_ICON_SIZE[0]
            n = 1
            while n <= 5:
                if start_x + end_x * (n-1) >= mousepos[0] <= start_x + end_x * n: 
                    break
                n += 1  
                    
            weapon = self.current_ship.weapons.select_from_key(str(n-1))
            data = self.current_ship.weapons.data[weapon]
            
            tooltip.append(weapon.capitalize())
            tooltip.append('speed: ' + str(data['speed']))
            tooltip.append('damage: ' + str(round(data['shield_damage'] * self.current_ship.fit('wep dmg'),2)) + '/' + str(round(data['armour_damage'] * self.current_ship.fit('wep dmg'), 2)))
            tooltip.append('speed: ' + str(data['speed']))
            tooltip.append('range: ' + str(data['range'] * self.current_ship.fit('wep range')))
            tooltip.append('activation: ' + str(data['activation']))
            
        elif self.max_resource_rect.collidepoint(mousepos):
            tooltip.append('Planetary resources: ' + str(sum(self.planet.resources.values())) + '/' + str(self.planet.resources_max))
            
        if tooltip:
            self.draw_mouseover_text(screen, tooltip)
            
    def draw_resource_bar(self, screen):
        
        xy = (OFFSET, WEAPON_ICON_SIZE[1] + OFFSET*2)

        pygame.draw.rect(screen, 'white', self.max_resource_rect, 1)    

        rect = (xy, (sum(self.planet.resources.values()) * RESOURCE_BAR, RESOURCE_BAR))
        pygame.draw.rect(screen, 'white', rect)   


    def get_mouse_text(self):
        
        text = self.selected_item.description(self.current_ship.scanner_lvl())
        if isinstance(text, list):
            return text
        else:
            return [text]


    def get_local_allies(self): # FIXME: This needed/can be consolodated?
        allies = []
        for mob in self.mobs:
            if mob.object_type() == 'Ship' and not mob.is_npc:
                allies.append(mob)
        return allies   
    

   




            


        
        
        
        
