#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: avicenna
"""

import numpy as np

def split_at_values(lst, values):
    indices = [i for i, x in enumerate(lst) if x in values]
    for start, end in zip([-1, *indices], [*indices, len(lst)]):
        yield lst[start+1:end]


with open('input1.txt','r') as fp:
    
    lines = fp.readlines()
    
