#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from adventofcode2021.utils import SnailNumberTree


def solve_problem1(input_path):
    
    lines = list(map(str.strip,open(input_path,'r').readlines()))
    
    tree1 = SnailNumberTree(lines[0])
    
    for line in lines[1:]:
        tree2 = SnailNumberTree(line)
        tree1 = tree1.join_to(tree2)
        
    return tree1.sum()    
        

if __name__ == '__main__':
    
    test_sum1 = solve_problem1('test_input1.txt')
    test_sum2 = solve_problem1('test_input2.txt')
    test_sum3 = solve_problem1('test_input3.txt')
    test_sum4 = solve_problem1('test_input4.txt')
    test_sum5 = solve_problem1('test_input5.txt')
    
    assert test_sum5 == 4140
    assert test_sum4 == 3488
    assert test_sum3 == 1137
    assert test_sum2 == 791
    assert test_sum1 == 445
    
    sum1 = solve_problem1('input1.txt')
    
    assert sum1 == 3486
    print(sum1)