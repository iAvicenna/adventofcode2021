#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from adventofcode2021.utils import split_list, binary_to_decimal

def print_image(image,path=None):
    
    s1 = image.shape[0]
    
    if path is not None:
        
        fp = open(path,'w')
    
    for i in range(s1):
        
        print(''.join(list(image[i,:])))
        
        if path is not None:
            fp.writelines(''.join(list(image[i,:]))+'\n') 
        
    fp.writelines('\n')
    fp.close()
    print('\n')

def extend_image(image, border='.', extra=0):
    
    arr = (image != border).astype(int)
    
    I = list(np.max(arr,axis=0).flatten())
    
    ind0 = I.index(1)
    ind1 = I[::-1].index(1)
    
    buf_left = max([2-ind0, 0])+extra
    buf_right = max([2-ind1, 0])+extra
    
    I = list(np.max(arr,axis=1).flatten())
    
    ind0 = I.index(1)
    ind1 = I[::-1].index(1)
    
    buf_top = max([2-ind0, 0])+extra
    buf_bottom = max([2-ind1, 0])+extra
    
    
    s1 = len(image) + buf_top + buf_bottom
    s2 = len(image[0]) + buf_right + buf_left
    
    
    new_image = np.zeros((s1,s2),dtype=str)     
    
    new_image[:,:] = border
    
    new_image[buf_top:s1-buf_bottom,buf_left:s2-buf_right] = np.array(image)
    
    return new_image


def solve_problem1_2(input_path,N):
    
    input_lines = list(map(str.rstrip,open(input_path,'r').readlines()))
        
    algorithm = ''.join(split_list(input_lines,'')[0])
    input_image = np.array([list(x) for x in split_list(input_lines,'')[1]])
    
    image = extend_image(input_image)
    corrected_image = image.copy()
    counter = 0
    
    border_map = {}
    
    border_map['.'] = algorithm[binary_to_decimal([0 for _ in range(9)])]
    border_map['#'] = algorithm[binary_to_decimal([1 for _ in range(9)])]
    
    border = '.'
    
    while counter<N:
        
        s1,s2 = image.shape
        
        corrected_image[0,:] = border_map[border]
        corrected_image[s1-1,:] = border_map[border]
        
        corrected_image[:,0] = border_map[border]
        corrected_image[:,s2-1] = border_map[border]
        
        
        for i in range(1,s1-1):
            for j in range(1,s2-1):
                
                pix_arr = ''.join(list(image[i-1:i+2,j-1:j+2].flatten())).replace('.','0').replace('#','1')
                index = binary_to_decimal([int(x) for x in pix_arr])
                corrected_image[i,j] = algorithm[index]
                
        border = border_map[border]
    
        corrected_image = extend_image(corrected_image,border=border)
        image = corrected_image.copy()
        counter += 1
        
    return np.count_nonzero(image=='#')
    
    
if __name__ == '__main__':
    
    test_val1 = solve_problem1_2('test_input1.txt',2)
    test_val2 = solve_problem1_2('test_input1.txt',50)
    
    assert test_val1 == 35
    assert test_val2 == 3351
    
    val1 = solve_problem1_2('input1.txt',2)
    
    print('Problem 1')
    print(f'Number of lit pixels {val1}')    
    assert val1 == 5425

    val2 = solve_problem1_2('input1.txt',50)
    print('Problem 2')
    print(f'Number of lit pixels {val2}')
    
    assert val2 == 14052