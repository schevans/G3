#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 18:25:49 2024

@author: steve
"""


class Point:

    def __init__(self, x, y=None):
        if y == None:
            if type(x) == Point:
                self.x = x.x
                self.y = x.y
            else:
                self.x = x[0]
                self.y = x[1]
        else:
            self.x = x
            self.y = y
            
    def __call__(self):
        return (self.x, self.y)