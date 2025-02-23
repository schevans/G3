#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 19:11:19 2024

@author: steve
"""
import pygame
from pygame.math import Vector2



class RotatableImage():
    
    def __init__(self, center, image, angle_deg=0):
        self.center = Vector2(center)
        self.original_image = image        
        self.angle_deg = angle_deg
        self.width, self.height = image.get_size()
        
    def update(self, center, angle_deg):
        self.center = Vector2(center)
        self.angle_deg = angle_deg
        
    def draw(self, screen):
        
        rotated_image = pygame.transform.rotate(self.original_image, self.angle_deg)
        
        width, height = rotated_image.get_size()
        
        topleft = ((self.center.x-width/2), (self.center.y-height/2))

        new_rect = rotated_image.get_rect(center = rotated_image.get_rect(topleft = topleft).center)

        screen.blit(rotated_image, new_rect)
        
    def change_color(self, old_color, new_color):
        width, height = self.original_image.get_size()
        old_red, old_green, old_blue, _ = old_color
        new_red, new_green, new_blue, _ = new_color
        for x in range(width):
            for y in range(height):
                red, green, blue, alpha = self.original_image.get_at((x, y))
                if red == old_red and green == old_green and blue == old_blue:
                    self.original_image.set_at((x, y), pygame.Color(new_red, new_green, new_blue, alpha))