#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import numpy as np
from adventofcode2021.utils import Interval,Cube,Cuboid

def intersect(x,y):
    
    if x[1]<y[0] or x[0]>y[1]:
        return [x[0],x[0]-1]
    else:
        return [max(min(x[0],y[1]),-50),min(max(x[1],y[0]),50)]
    
    
def solve_problem1_2(input_path, restrict=False):
    
    input_lines = list(map(str.strip,open(input_path,'r')))
    commands = ['on'*('on' in x)+'off'*('off' in x) for x in input_lines]
    
    cuboid = Cuboid()
    
    for ind,input_line in enumerate(input_lines):
        split_input = [list(map(int,x.replace('on ','').split('=')[-1].split('..'))) for x in input_line.split(',')]
        
        cube = Cube(Interval(*split_input[0]),Interval(*split_input[1]),Interval(*split_input[2]))
        
        if restrict:
            cube0 = Cube(Interval(-50,50),Interval(-50,50),Interval(-50,50))
            cube = cube.intersection(cube0)
        
        command = commands[ind]
        if command=='on':
            cuboid.add_cubes([cube])
        elif command=='off':
            cuboid.difference(cube)
            
    return cuboid.vol()


if __name__ == '__main__':
    
    test_count1 = solve_problem1_2('test_input1.txt', restrict=True)
    test_count2 = solve_problem1_2('test_input2.txt', restrict=True)
    test_count3 = solve_problem1_2('test_input3.txt', restrict=True)

    assert test_count1 == 39
    assert test_count2 == 590784
    assert test_count3 == 474140
    
    count = solve_problem1_2('input1.txt', restrict=True)
    
    print(f'Problem 1 result {count}')
    assert count == 547648
    
    test_count1 = solve_problem1_2('test_input3.txt')

    assert test_count1 == 2758514936282235
    
    #takes about 50 seconds in intel i7
    count = solve_problem1_2('input1.txt')
    
    print(f'Problem 2 result {count}')
    assert count == 1206644425246111