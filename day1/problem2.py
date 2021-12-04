#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def solve_problem2(input_path):
    
    with open(input_path,'r') as fp:
        
        lines = fp.readlines()
    
    numbers = [int(x) for x in lines]
    
    sum_numbers = [sum(numbers[i:i+3]) for i in range(len(numbers)-2)]
    
    dif = [x1-x0 for x0,x1 in zip(sum_numbers[:-1],sum_numbers[1:])]
    
    print(len([x for x in dif if x>0]))
    
if __name__ == '__main__':
    
    solve_problem2('./test_input.txt')
    solve_problem2('./input1.txt')