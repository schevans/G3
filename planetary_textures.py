#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 19:27:39 2025

@author: steve
"""

import pygame
import opensimplex
import numpy as np
import random

import utils

WIDTH = 1200
HEIGHT = 800
CENTER = [WIDTH/2, HEIGHT/2]


pygame.init()

screen = pygame.display.set_mode((WIDTH,HEIGHT))

clock = pygame.time.Clock()


FEATURE_SIZE = 40

size = 200
r = 100
S = r
x0 = 50
y0 = 50
z0 = 50
#rng = numpy.random.default_rng(seed=0)

#ix, iy, iz= rng.random(size), rng.random(size), rng.random(size),

# lava
color1 = pygame.Color('yellow')
color2 = pygame.Color('brown')
lava = 10*40

# earth-like
#color1 = pygame.Color('green')
#color2 = pygame.Color('blue')
#planet = M

# ocean
#color1 = pygame.Color('lightblue')
#color2 = pygame.Color('blue')
# A*M

# rocky
#color1 = pygame.Color('brown4')
#color2 = pygame.Color('darkorange3')
# A*M


def print_array(array, x_offset, y_offset=50):
    for y in range(0, size):
        for x in range(0, size):
            
            color = (0, int((array[x,y] + 1) * 128), 0)

            screen.set_at((x+x_offset, y+y_offset), color)
            
            
def print_thing(array, x_offset, y_offset=50):
    for y in range(0, size):
        for x in range(0, size):
            
            #value = array[x,y]
            ratio = (array[x,y] + 1) / 2
            color = ( color2 * ratio ) + ( color1 * ( 1- ratio))
            
            utils.fade_color_to(color1, color2, ratio )
            
            # lerp(Color, float) -> Color
            
            screen.set_at((x+x_offset, y+y_offset), color)
            
#value = opensimplex.noise3array(ix, iy, iz)

def clamp(n, smallest, largest): return max(smallest, min(n, largest))
def butterfly(n, smallest, largest): return max(largest, min(n, smallest))

FEATURE_SIZE = 10
LARGE = 40

A = np.zeros([size, size])
M = np.zeros([size, size])
E1 = np.zeros([size, size])
E2 = np.zeros([size, size])
E3 = np.zeros([size, size])


random.seed(44)
clamp_low = (random.random() -0.5 ) * 2
clamp_high = clamp_low + 0.1 # (random.random() +0.5 ) * 2 # random.random()  # clamp_low + 0.1
if clamp_low > clamp_high:
    clamp_low, clamp_high = clamp_high, clamp_low 

print(clamp_low, clamp_high)


for y in range(0, size):
    for x in range(0, size):
            
        #r = math.sqrt(math.pow(x-x0, 2) + math.pow(y-y0, 2) + math.pow(z-z0, 2))

        #if r == 50:
        #if math.isclose(r, 50, abs_tol=2):
        A[x,y] = opensimplex.noise2(x/FEATURE_SIZE,y/FEATURE_SIZE)
        M[x,y] = opensimplex.noise2(x/LARGE,y/LARGE)   

        E1[x,y] = M[x,y] * A[x,y] 

        R = 2; # Higher for less mountains.
        A[x,y] = pow(A[x,y],R);

        #E2[x,y] = M[x,y] * A[x,y]
        P = 2   # Higher for stronger bias.  
        E2[x,y] = M[x,y] * pow(A[x,y]*2,P)/2 if A[x,y]  < 0 else 1-(pow((1-A[x,y])*2,P)/2)
        #E = M*(A<0.5?power(A*2,P)/2:1-(power((1-A)*2,P)/2));

        E3[x,y] = clamp(E2[x,y], clamp_low, clamp_high)

        #warpstrength = 1
        #dx = warpstrength * opensimplex.noise2(x+123, y+456)
        #dy = warpstrength * opensimplex.noise2(x-789, y-456)
        #E3[x,y] = opensimplex.noise2( x + dx, y + dy);



        #value = (value1 + value2 ) /2 

        #color = (0, int((value + 1) * 128), 0)
        #screen.set_at((x+x0, y+y0), color)


                    
                #screen.set_at((x+x0, y+y0), 'green')

#np.save('./moo.txt', A)

print_thing(A, x0)
print_thing(M, size + x0*2)        
print_thing(E1, size*2 + x0*3)   
print_thing(E2, size*3 + x0*4)   
print_thing(E3, x0, size + y0*2 )   
    

PLANET_VIEW_RADIUS_MULT = 8  # FIXME: Dup im planets
mapHeight = 100

time = 0
rotationSpeed = 1

def get_image(planet):
    
    planet_view_r = planet.size * PLANET_VIEW_RADIUS_MULT * 2
    
    surface1 = pygame.Surface((planet_view_r, planet_view_r), pygame.SRCALPHA)
    surface2 = pygame.Surface((planet_view_r, planet_view_r), pygame.SRCALPHA)
    surface3 = pygame.Surface((planet_view_r, planet_view_r), pygame.SRCALPHA)
    
    for x in range(planet_view_r):
        for y in range(planet_view_r):
            print(x,y)
            
            px = x * 2/planet_view_r - 1
            py = y * 2/planet_view_r - 1
            
            magSq = px * px + py * py
            
            if ( magSq > 1 ):
                continue
            
            pxo = px
            pyo = py
            
            # lens distortion
            scale = 0.35 * magSq + (1 - 0.35)
            px = px * scale
            py = py * scale
            
            # convert our local offsets into lookup coordinates into our map texture
            u = time * rotationSpeed + (px + 1) * (mapHeight/2) 
            v = (py + 1) * (mapHeight/2)
            # wrap the horizontal coordinate around our map when it goes off the edge
            u = u % (2 * mapHeight)
            
            # convert our local offsets into lookup coordinates into our map texture
            uo = time * rotationSpeed + (pxo + 1) * (mapHeight/2) 
            vo = (pyo + 1) * (mapHeight/2)
            # wrap the horizontal coordinate around our map when it goes off the edge
            uo = uo % (2 * mapHeight)
            
            moo = E1[int(u)][int(v)]
            color1 = (0, (int(E1[int(u)][int(v)] + 1) * 128), 0)
            coloro = (0, (int(E1[int(uo)][int(vo)] + 1) * 128), 0)
        
            moo = ( moo + 1 ) / 2 # normal
            t1 = 207
            t2 = 1 + 206 * moo
            t3 = 21 * moo
        
            newcolor = ( t1, t2, t3 )
        
        
                
            #print(newcolor)
            surface1.set_at((x, y), pygame.Color('white'))
            surface2.set_at((x, y), newcolor)
            surface3.set_at((x, y), coloro)
         
        #surface2.fill('blue')

            
    return surface2

class Planet():
    
    def __init__(self, size):
        
        self.size = size

planet = Planet(10)

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        
    surface = get_image(planet)
    screen.blit(surface, (500, 500))
    
    time += 1
    #spin += 1
    
    pygame.display.flip()  # Refresh on-screen display
    clock.tick(24)        
          



          
"""

print('Generating 2D image...')

rng = numpy.random.default_rng(seed=0)
ix, iy = rng.random(100), rng.random(100)
opensimplex.noise2array(ix, iy)

print('done1')

pos = 0
neg = 0

FEATURE_SIZE = 5

size = 300
r = 100
S = r
for y in range(0, size):
    for x in range(0, size):
        center = (size/2, size/2)
        
        rx = math.sqrt((x-center[0])**2 + (y-center[1])**2) / r
        
        rx = rx *2
        
        tmp = 0.5
        
        if rx != 0:
            
            value = opensimplex.noise2((x / (FEATURE_SIZE/rx))+tmp, (y / (FEATURE_SIZE/rx)+tmp))
            #value = opensimplex.noise2(2*x / FEATURE_SIZE, y / FEATURE_SIZE)
            color = (0, int((value + 1) * 128), 0)
            screen.set_at((x, y), color)
            
            longitude = math.radians(x)
            latitude = math.radians(y)
            
            #r = sqrt( x^2 + y^2 + z^2 )
            #theta = arctan( y/x )
            #phi = arccos( z/r )
            # treat theta as longitude and phi as latitude
            
            
            #longitude = x / r
            #latitude = 2 * math.atan(math.exp(y/r)) - math.pi/2
            
            Px = S * math.cos(latitude) * math.cos(longitude)
            Py = S * math.cos(latitude) * math.sin(longitude)
            Pz = S * math.sin(latitude)
        
            screen.set_at((x, y), color)
            
            screen.set_at((400+round(Px), 200+round(Py)), color)
        
            if Pz > 0:
                pos += 1
            elif Pz <= 0:
                neg += 1
            
        
        
        
print('done2', pos, neg)






    
    
"""  
    