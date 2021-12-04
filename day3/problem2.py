#!/usr/bin/env python3
# -*- coding: utf-8 -*-



import numpy as np
from adventofcode2021 import utils


def filter_array(arr, ind, ftype='more'):
    
    s1,_ = arr.shape
    
    mean = np.mean(arr[:,ind],axis=0)
    mean += (mean==0.5)*1e-10
    
    i0 = int(np.round(mean.flatten()))
    
    if ftype=='less':
        i0 = 1-i0
    
    J = [i for i in range(s1) if arr[i,ind]==i0]
    
    return arr[J,:]
     

def solve_problem2(input_path):
    
    with open(input_path,'r') as fp:
        
        lines = fp.readlines()
        
    arr = []
    
    for line in lines:
        arr.append([int(x) for x in line.strip('\n')])
    
    arr = np.array(arr) 
       
    new_arr = arr.copy()
    counter = 0
    
    while new_arr.shape[0] != 1:
        new_arr = filter_array(new_arr,counter)
        counter += 1
        
    ogr = utils.binary_to_decimal(list(new_arr.flatten()))
    
    new_arr = arr.copy()
    counter = 0
    while new_arr.shape[0] != 1:
        new_arr = filter_array(new_arr,counter,ftype='less')
        counter += 1
        
    cgr = utils.binary_to_decimal(list(new_arr.flatten()))
    
    
    print(ogr*cgr)


if __name__ == '__main__':
    
    solve_problem2('./test_input.txt')        
    solve_problem2('./input1.txt')       
    
