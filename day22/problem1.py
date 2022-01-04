#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import itertools as it
import numpy as np

def intersect(x,y):
    
    if x[1]<y[0] or x[0]>y[1]:
        return [x[0],x[0]-1]
    else:
        return [max(min(x[0],y[1]),-50),min(max(x[1],y[0]),50)]
    
def solve    
    
input_lines = list(map(str.strip,open('test_input2.txt','r')))
commands = ['on'*('on' in x)+'off'*('off' in x) for x in input_lines]

grid = np.zeros((101,101,101),dtype=bool)

for ind,input_line in enumerate(input_lines):
    split_input = [list(map(int,x.replace('on ','').split('=')[-1].split('..'))) for x in input_line.split(',')]

    split_input = [intersect(x,[-50,50]) for x in split_input]
    
    switch = list(it.product(range(split_input[0][0],split_input[0][1]+1), range(split_input[1][0],split_input[1][1]+1), range(split_input[2][0],split_input[2][1]+1)))
    switch = tuple(list(np.array(switch).T+50))
   
    if len(switch)>0:
        grid[switch] = commands[ind] == 'on' 

    print(f'{ind} {np.count_nonzero(grid)}')