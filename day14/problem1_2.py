#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from adventofcode2021.utils import Polymer

def solve_problem1_2(input_path, Niter):
    
    with open(input_path,'r') as fp:
        
        lines = fp.readlines()
    
    initial = lines[0].strip('\n')    
        
    polymerization_dict = {}
    
    for line in lines[2:]:
        line = line.strip('\n')
        polymerization_dict[line.split(' -> ')[0]] = line.split(' -> ')[1]
    
    polymer = Polymer(initial, polymerization_dict)
    n = 0
    
    while n<Niter:
        polymer.polymerize()
        n += 1
        
    print(polymer.score())
        
    
if __name__ == '__main__':
    
    solve_problem1_2('test_input.txt',10)
    solve_problem1_2('input1.txt',10)
    solve_problem1_2('input1.txt',40)