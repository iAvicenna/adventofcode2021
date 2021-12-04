#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
from adventofcode2021 import utils

def solve_problem1(input_path):
    with open(input_path,'r') as fp:
        lines = fp.readlines()
              
    arr = []
    
    for line in lines:
        arr.append([int(x) for x in line.strip('\n')])
    
    arr = np.array(arr)    
    
    mean = np.mean(arr,axis=0)
    
    gamma = [int(np.round(x)) for x in mean]
    eps = [1 if x==0 else 0 for x in gamma]
    
    gamma_dec = utils.binary_to_decimal(gamma)
    eps_dec = utils.binary_to_decimal(eps)
    print(gamma_dec*eps_dec)
    
    
if __name__ == '__main__':
    
    solve_problem1('./test_input.txt')
    solve_problem1('./input1.txt')