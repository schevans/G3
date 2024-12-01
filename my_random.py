#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 18:17:39 2024

@author: steve
"""


import random

import constants as const

random.seed(const.random_seed)


def my_random():
    return random.random()


def my_randint(low, high):
    return random.randint(low,high)


def my_choices(mylist, weights=None, cum_weights=None, k=1):
    return random.choices(mylist, weights=weights, cum_weights=cum_weights, k=k)


