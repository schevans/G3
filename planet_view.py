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
from game_view import GameView, View
from explosions import Explosion, LootBox

DOCK_RADIUS = 15
LOCK_RADIUS = 10

LEFT_MOUSE_CLICK = 1
RIGHT_MOUSE_CLICK = 3

def unobstructed_view(xy1, xy2, cpt, r):
    
    if xy1.distance_to(cpt) > xy1.distance_to(xy2):
        return True
    else:
        return not line_intersects_circle(xy1, xy2, cpt, r)
            
def line_intersects_circle(xy1, xy2, cpt, r):
    
    x1 = xy1[0] - cpt[0]
    y1 = xy1[1] - cpt[1]
    x2 = xy2[0] - cpt[0]
    y2 = xy2[1] - cpt[1]
    
    dx = x2 - x1
    dy = y2 - y1
    dr = math.sqrt(dx*dx + dy*dy)
    D = x1 * y2 - x2 * y1
    discriminant = r*r*dr*dr - D*D

    return discriminant >= 0

class PlanetView(GameView):

    def __init__(self):
        GameView.__init__(self)
        
        
    def cleanup(self):
        self.mobs = []

    def startup(self, shared_dict):
        self.shared_dict = shared_dict
        self.shared_dict['history'].append(View.PLANET)
        self.current_ship = self.shared_dict['current_ship']
        self.planet = shared_dict['planet']
        self.planet_r = self.planet.size*8
        
        angle_radians = 0
        
        applicable_mobs = []
        
        for ship in self.ships:
            if ship.planet == self.planet:
                applicable_mobs.append(ship)
           
        if applicable_mobs:
            angle_increment = ( math.pi * 2 ) / len(applicable_mobs)
            
            for mob in applicable_mobs:                                 
                angle_radians += angle_increment
                self.mobs.append(OrbitalShip(mob, self.planet, self.get_random_r(), angle_radians))

        self.is_paused = False 

    def process_event(self, event):
        
        GameView.process_event(self, event)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.shared_dict['system'] = self.planet.system
                self.next_view = (View.SOLAR, self.shared_dict)
            if event.key == pygame.K_SPACE:
                self.is_paused = not self.is_paused
            if event.key == pygame.K_w:
                for mob in self.mobs:
                    if mob.name != 'Hero' and self.mobs[0].xy.distance_to(mob.xy) < DOCK_RADIUS:
                        mob.tmpship.recruit()  # FIXME: Better solution (tmpship - conjoined with orbital_ship)
                        self.shared_dict['other_ship'] = mob
                        self.next_view = (View.DOCKING, self.shared_dict)
            if pygame.key.name(event.key) in ['1', '2', '3', '4', '5']:
                self.mobs[0].weapons.select(pygame.key.name(event.key))
                
        #if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT_MOUSE_CLICK:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSLASH:        
            self.lock_target(self.mobs[0], pygame.mouse.get_pos())
        #if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_CLICK:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            bullet = self.mobs[0].shoot()
            if bullet:
                self.mobs.append(bullet)
                        
        keys = pygame.key.get_pressed() 
        self.mobs[0].acceleration = 0
        if keys[pygame.K_d]:
            self.mobs[0].acceleration  = 1
        if keys[pygame.K_a]:        
            self.mobs[0].acceleration  = -1  
                        
    def update(self):
        if not self.is_paused:
            GameView.update(self)
 
        self.do_ai()   
 
        self.get_selected_item(self.mobs)
        
        for mob in self.mobs:
            if mob.object_type() == 'Ship':
                
                if mob.locked_target:
                    # break lock?
                    if not unobstructed_view(mob.xy, mob.locked_target.xy, const.screen_center, self.planet_r):
                        mob.locked_target = None
                    
                # has been hit by bullet?
                for bullet in (x for x in self.mobs if x.object_type() == 'Bullet' and not x.homing):
                    if bullet.xy.distance_to(mob.xy) <= const.weapon_hit_radius:
                        bullet.hit(mob)
                        
                # has picked up lootbox?
                for lootbox in (x for x in self.mobs if x.object_type() == 'LootBox'):
                    if lootbox.xy.distance_to(mob.xy) <= const.weapon_hit_radius:
                        mob.loot(lootbox)
                        
                # has ship hit planet?      
                if mob.r <= self.planet_r:
                    mob.hit(3,3)
                    mob.r += 5  # and bounce
                        
            # has bullet hit planet => mining
            elif mob.object_type() == 'Bullet' and mob.is_alive:
                if mob.xy.distance_to(const.screen_center) <= self.planet_r:
                    resources = self.planet.mine(mob)
                    mob.is_alive = False
                    if resources:
                        r = self.planet_r * 4
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
                elif mob.object_type() == 'Explosion':
                    self.mobs.append(LootBox(mob.xy, mob.resources))
                
        
        

    def draw(self, screen):
        
        GameView.draw(self, screen)
        self.planet.draw(screen, self.planet_r)
        GameView.draw_objects(self, screen)
        
        self.mobs[0].weapons.draw_icons(screen,self.mobs[0].resources )
        
        if self.is_paused:
            text = '[ Paused ]'
            text_surface = utils.fonts[30].render(text, True, 'white', 'black')
            text_width, text_height = text_surface.get_size()
            text_pos = Vector2(const.screen_width / 2 - text_width / 2, text_height + 10)
            screen.blit(text_surface, text_pos )
            

    def get_mouse_text(self):
        
        text = self.selected_item.description()
        if isinstance(text, list):
            return text
        else:
            return [self.selected_item.description()]


    def get_local_allies(self):
        allies = []
        for ship in self.ships:
            if not ship.is_npc and ship.planet == self.current_ship.planet:
                allies.append(ship)
        return allies   
    
    def get_random_r(self):
        r = int(my_random.my_gauss() * ( const.screen_height/2 - self.planet_r + const.ship_width ) + 40)
        
        for mob in self.mobs:
            if math.isclose(r, mob.r, abs_tol=const.ship_width):
                return self.get_random_r()
        return r

   


    def lock_target(self, ship, xy):

        for mob in self.mobs:
            if mob.xy.distance_to(xy) <= LOCK_RADIUS:
                if unobstructed_view(self.ship.xy, mob.xy, const.screen_center, self.planet_r):
                    ship.locked_target = mob
        

    def do_ai(self):


        for mob in self.mobs:
            if mob.object_type() == 'Ship' and mob.is_alive and mob.is_npc:
                
                if mob.locked_target:
                   bullet = mob.do_ai()
                   if bullet:
                       self.mobs.append(bullet)
                       
                elif mob.ai_target:
                    self.lock_target(mob, mob.ai_target.xy)
                
                else:
                    enemies = []
                    for enemy in self.mobs:
                        if enemy.object_type() == 'Ship' and enemy.is_alive and not enemy.is_npc:
                            enemies.append(enemy)
                    enemies.sort(key=lambda x: x.xy.distance_to(enemy.xy))
                    if enemies:
                        mob.ai_target = enemies[0]
            


        
        
        
        