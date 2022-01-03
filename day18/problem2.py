#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools as it
import time
from adventofcode2021.utils import SnailNumberTree


def solve_problem1(input_path):
    
    lines = list(map(str.strip,open(input_path,'r').readlines()))
    
    snail_trees = [SnailNumberTree(lines[i]) for i in range(len(lines))]
    

    I = list(it.combinations(range(len(lines)), 2))
    max_val = 0
    counter = 0
    sum1 = 0
    sum2 = 0
    

    for i0,i1 in I:
        
        if counter%100==0 and counter>0:
            print(f'%{100*counter/len(I):.0f} complete')
        
        
        tree1 = snail_trees[i0].join_to(snail_trees[i1])        
        sum1 = tree1.sum()
        
        tree2 = snail_trees[i1].join_to(snail_trees[i0])        
        sum2 = tree2.sum()
        
        
        max_val = max([sum1, sum2, max_val])
        counter += 1
        
    return max_val
        

if __name__ == '__main__':
    

    test_val1 = solve_problem1('test_input4.txt')
    test_val2 = solve_problem1('test_input5.txt')
    
    assert test_val1 == 3805
    assert test_val2 == 3993

    '''
    takes about 80 seconds on intel core i7
    '''
        
    max_val = solve_problem1('input1.txt')

    assert max_val == 4747