#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import itertools as it
from adventofcode2021.utils import split_list

def inv_div(a,b):
        
    return [a*b + n for n in range(0,b,1)]
    

def fun(divz, addy, addx, z, w):
    
    '''
    Each instruction can be written as a function of this form, only used
    to check that fun o fun_inv = id
    '''
    
    x = (z%26 + addx)
    
    if x==w:
        return int(z//divz)   #= znext
    else:
        return 26*int(z//divz) + w + addy  #= znext
    
    
def fun_inv(divz, addy, addx, znext, w):
    
    '''
    each operation for monad has similiar structure with differing denominators
    for z and different added values to y and x. This encapsulates the
    inverse function for each block and given the result z and w input for the
    previous level, produces all the possible z values for the previous level
    which would produce the given z result.
    '''
    
    prev_z = []
    
    zvals1 = inv_div(znext, divz)
    zval2 = znext - addy - w
    zvals2 = []
    
    if zval2%26==0:
        zvals2 = inv_div(zval2/26, divz)
        
    for zval in zvals1:
        if zval%26 + addx == w:
            prev_z.append(int(zval))
    
    for zval in zvals2:
        if zval%26 + addx != w:
            prev_z.append(int(zval))
        
    return prev_z

def solve_problem1_2(input_path, problem=1):
    
    '''
    starting with the final assumption that z=0, for each possible w input for the last level
    find all the z values which when the instruction is applied would give z=0. 
    
    Then repeat the same going backwards one level at a time. To make it faster, 
    for problem 1 only w which would produce the largest 
    model no is kept where as for problem 2 only those which would produce the smallest
    model no is kept (by reversing the direction of w range)
    '''
    
    
    input_lines = split_list(list(map(str.rstrip,open('input1.txt','r'))),'inp w')[1:]
    
    divz_list = []
    addy_list = []
    addx_list = []
    
    for ind0, instructions in enumerate(input_lines):
        for ind1, instruction in enumerate(instructions):
            if ind1==4:
                addx_list.append(int(instruction.split(' ')[-1]))
            if ind1==14:
                addy_list.append(int(instruction.split(' ')[-1]))
            if ind1==3:
                divz_list.append(int(instruction.split(' ')[-1]))
     
    
    N = len(divz_list)
    zs = {0}
    
    results = {}
    prev_pairs = {}
    nodes = []
    
    if problem == 1:
        wrange = range(1,10)
    else:
        wrange = range(9,0,-1)
    
    
    for i in range(N-1,-1,-1):
        
        divz = divz_list[i]
        addy = addy_list[i]
        addx = addx_list[i]
                        
        prev_pairs[i] = {}
        
        prev_zs = []
    
    
        for w,z in it.product(wrange,zs):
            
                
            results = fun_inv(divz, addy, addx, z, w)
    
            if len(results)>0:
                    
                for z2 in results:
                    if i==N-1:
                        name = f'{w},{z}'
                    else:
                        name = prev_pairs[i+1][z] + f'/{w},{z}'
                        
                    nodes.append(name)           
                    prev_pairs[i][z2] = name
                        
            prev_zs += results
            
        zs = set(prev_zs)
    
    results = []
    for node in nodes:
        if node.count('/') == N-1:
            parts = node.split('/')
            
            parts = [x.split(',')[0] for x in parts]
            results.append(''.join(parts[::-1]))
            
    if problem==1:
        return int(max(results))
    else:
        return int(min(results))
            
if __name__ == '__main__':
    
    result1 = solve_problem1_2('input1.txt',1)
    print(f'Problem 1 solutions is {result1}')
    assert result1==59998426997979
    
    result2 = solve_problem1_2('input1.txt',2)
    print(f'Problem 2 solutions is {result2}')
    assert result2==13621111481315
    