#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

def solve_problem1(input_path):
        
    with open(input_path,'r') as fp:
        
        lines = fp.readlines()
        
    positions = np.array([int(x.strip('\n')) for x in lines[0].split(',')], dtype=int)
    
    max_x = max(positions)
    
    grid = np.tile(np.reshape(np.array(range(0,max_x),dtype=int), (max_x,1)),(1,len(positions)))
    
    tiled_positions = np.tile(positions, (grid.shape[0],1))
    
    costs = np.sum(np.abs(grid-tiled_positions),axis=1).astype(int)
    
    I = np.argmin(costs)
    print(f'Position {I} with cost {costs[I]}')


if __name__ == '__main__':
    
    solve_problem1('./test_input.txt')
    solve_problem1('./input1.txt')
