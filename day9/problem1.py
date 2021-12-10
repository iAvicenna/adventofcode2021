#!/usr/bin/env python3
# -*- coding: utf-8 -*-

input_path = 'input1.txt'
import numpy as np

def solve_problem1(input_path):  
    with open(input_path,'r') as fp:
        
        lines = fp.readlines()
        
     
    s1 = len(lines)
    s2 = len(lines[0].strip('\n'))
    
    height_map = 10*np.ones((s1+2,s2+2),dtype=int)
    
    for ind,line in enumerate(lines):
        height_map[ind+1,1:s2+1] = [int(x) for x in line.strip('\n')]
        
    is_low = np.zeros((s1,s2),dtype=bool)
    filter_M = np.array([[False,True,False],[True,False,True],[False,True,False]])
    
    for i0 in range(1,s1+1):
        for i1 in range(1,s2+1):
            val = height_map[i0,i1]
            is_low[i0-1,i1-1] = all(val<x for x in height_map[i0-1:i0+2,i1-1:i1+2][filter_M])
            
     
    low_vals = height_map[1:s1+1,1:s2+1][is_low] 
    print(np.sum(low_vals+1))

if __name__ == '__main__':
    
    solve_problem1('./test_input.txt')
    solve_problem1('./input1.txt')
