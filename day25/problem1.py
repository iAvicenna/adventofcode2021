#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 30 20:56:09 2021

@author: avicenna
"""
import numpy as np


def solve_problem1(input_path):
    
    '''
    not much to this. using roll functionality on np arrays,
    checks which cucumbers to move and then move them
    '''
    
    state = np.array(list(map(list,map(str.rstrip,open(input_path,'r')))))
    fixed_point = False
    counter = 0
    
    while not fixed_point:

        init_state = state.copy()
        
        state_ls = np.roll(state,-1,axis=1)
        I1 = np.logical_and(state == '>', state_ls == '.')
        I2 = np.roll(I1,1,axis=1)
        
        
        state[I1] = '.'
        state[I2] = '>'
    
        state_ds = np.roll(state,-1,axis=0)
        I1 = np.logical_and(state == 'v', state_ds == '.')
        I2 = np.roll(I1,1,axis=0)
        
        
        state[I1] = '.'
        state[I2] = 'v'
        
        
        counter+=1
        
        if np.array_equal(state,init_state):
            fixed_point = True
            
    return counter

if __name__ == '__main__':
    
    test_result1 = solve_problem1('test_input1.txt')
    
    assert test_result1 == 58
    
    result1 = solve_problem1('input1.txt')
    print(f'Result is {result1}')
    assert result1 == 417