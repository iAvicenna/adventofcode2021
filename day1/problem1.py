#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def solve_problem1(input_path):
    
    with open(input_path,'r') as fp:
        
        lines = fp.readlines()
        
    numbers = [int(x) for x in lines]
    
    dif = [x1-x0 for x0,x1 in zip(numbers[:-1],numbers[1:])]
    
    print(len([x for x in dif if x>0]))
    
    

if __name__ == '__main__':
    
    solve_problem1('./test_input.txt')
    solve_problem1('./input1.txt')