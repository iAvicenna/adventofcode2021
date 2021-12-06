#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 11:32:20 2021

@author: avicenna
"""
import numpy as np


def solve_problem1_2(input_path,Ncycles):
    with open(input_path,'r') as fp:
        
        days = fp.readlines()
        
    days = np.array([int(x) for x in days[0].split(',')], dtype=int)
    
    counts = np.zeros((9,),dtype=int) #days range from 0 to 8
    
    for day in days:
        counts[day+1] +=1
    
    transfer_matrix = np.array([
        [0,1,0,0,0,0,0,0,0], #  0
        [0,0,1,0,0,0,0,0,0], #  1
        [0,0,0,1,0,0,0,0,0], #  2
        [0,0,0,0,1,0,0,0,0], #  3
        [0,0,0,0,0,1,0,0,0], #  4
        [0,0,0,0,0,0,1,0,0], #  5
        [1,0,0,0,0,0,0,1,0], #  6
        [0,0,0,0,0,0,0,0,1], #  7
        [1,0,0,0,0,0,0,0,0], #  8
        ],dtype=int)
    
    
    for i in range(Ncycles+1):
        
        counts = transfer_matrix@counts

    print(sum(counts))
        
if __name__=='__main__':
    
   solve_problem1_2('./test_input.txt',18) 
   solve_problem1_2('./test_input.txt',80)
   solve_problem1_2('./test_input.txt',256)
   
   solve_problem1_2('./input1.txt',80)
   solve_problem1_2('./input1.txt',256)