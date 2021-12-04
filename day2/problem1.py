#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def solve_problem1(input_path):
    
    with open(input_path,'r') as fp:
        
        lines = fp.readlines()
        
    split_lines = [x.strip('\n').split(' ') for x in lines]
    
    coords = [0,0]
    
    pd = {'forward':0,'down':1,'up':1}
    change = {'forward':1, 'down':1, 'up':-1}
    
    for x,y in split_lines:
        coords[pd[x]] += change[x]*int(y)
    
    print(coords[0]*coords[1])
    
if __name__ == '__main__':
    
    solve_problem1('./test_input.txt')
    solve_problem1('./input1.txt')