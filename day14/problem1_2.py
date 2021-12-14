#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def solve_problem1_2(input_path, Niter):
    
    with open(input_path,'r') as fp:
        
        lines = fp.readlines()
    
    initial = lines[0].strip('\n')    
        
    polymerization_dict = {}
    
    for line in lines[2:]:
        line = line.strip('\n')
        polymerization_dict[line.split(' -> ')[0]] = line.split(' -> ')[1]
    
    coords = list(polymerization_dict.keys())
    s1 = len(coords)
    transfer_matrix = np.zeros((s1,s1), dtype=int)
    semi_transfer_matrix = np.zeros((s1,s1), dtype=int)
    
    for i0,coord0 in enumerate(coords):
        
        coord1 = coord0[0] + polymerization_dict[coord0]
        coord2 = polymerization_dict[coord0] + coord0[1]
        
        i1 = coords.index(coord1)
        i2 = coords.index(coord2)
        
        transfer_matrix[i1,i0] = 1
        transfer_matrix[i2,i0] = 1
        
        semi_transfer_matrix[i1,i0] = 1
        
        
    vec = np.array([initial.count(x) for x in coords], dtype=int)
    
    for i in range(Niter):
        
        if i==Niter-1:
            count_vec = semi_transfer_matrix @ vec
        
        vec = transfer_matrix @ vec
        
        
    letter_counts = {x:0 for x in polymerization_dict.values()}

    for ind,count in enumerate(count_vec.flatten()):
        
        if count>0:
            coord = coords[ind]
            
            letter_counts[coord[0]] += count
            letter_counts[coord[1]] += count
        
    letter_counts[initial[-1]] += 1
        
    print(max(letter_counts.values()) - min(letter_counts.values()))
    
if __name__ == '__main__':
    
    solve_problem1_2('test_input.txt',10)
    solve_problem1_2('input1.txt',10)
    solve_problem1_2('input1.txt',40)