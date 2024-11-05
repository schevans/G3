#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 18:06:16 2024

@author: steve
"""

class MaxableAmount():
    
    def __init__(self, max_amount, amount=None):
        self.max = max_amount
        self.amount = amount if amount else max_amount
        
    def dec(self, change):      
        if self.amount >= change:
            self.amount -= change
            return True
        else:
            return False
        
    def inc(self, change):       
        self.amount = min(self.max, self.amount + change)
    
    def inc_max(self, max_amount, fill):
        self.max = max_amount
        if fill:
            self.amount = self.max
        
    def __call__(self):
        return self.amount

        
        
        