#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

def process_strlines(strline):
    
    
    x = [int(strline.split(' -> ')[0].split(',')[0]), int(strline.split(' -> ')[1].split(',')[0])]
    y = [int(strline.split(' -> ')[0].split(',')[1]), int(strline.split(' -> ')[1].split(',')[1])]
    
    return x,y

def generate_lines(xcoords, ycoords):
    
    line_points = []
    
    if xcoords[0] == xcoords[1]:
        line_points = [(xcoords[0],i) for i in range(min(ycoords),max(ycoords)+1)]

    elif ycoords[0] == ycoords[1]:
        line_points = [(i, ycoords[0]) for i in range(min(xcoords),max(xcoords)+1)]
        
    return line_points

def solve_problem1(input_path):
           
    with open(input_path,'r') as fp:
        str_lines = fp.readlines()
    
    all_line_points = []
    n_rows = 0
    n_cols = 0
    for str_line in str_lines:
        
        x,y = process_strlines(str_line)
        
        n_rows = max([max(y)+1,n_rows])
        n_cols = max([max(x)+1,n_cols])
        all_line_points.append(generate_lines(x,y))
    
    
    grid = np.zeros((n_rows,n_cols))
    
    for line_points in all_line_points:
        
        for line_point in line_points:
            grid[line_point[::-1]] += 1
    
    
    print(len(np.argwhere(grid>1)))


if __name__ == '__main__':
    
    solve_problem1('./test_input.txt')
    solve_problem1('./input1.txt')
