#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import itertools
import numpy as np
from adventofcode2021.utils import dijkstra

def solve_problem1_2(input_path,extend=False):

    lines = list(map(str.strip,open(input_path,'r')))
    lines = [list(map(int,line)) for line in lines]
    
    s1 = len(lines)
    s2 = len(lines[0])
    
    risk = np.array(lines)
    
    if extend:
        combined_risk = np.zeros((s1*5,s2*5),dtype=int)
        
        for i in range(5):
            for j in range(5):
                
                new_risk = (risk + (i+j))%9
                new_risk[new_risk==0] = 9
                        
                combined_risk[i*s1:(i+1)*s1,j*s2:(j+1)*s2] = new_risk
    else:
        combined_risk = risk
            
    s1,s2 = combined_risk.shape
    
    G = [[] for i in range(s1*s2)]
    
    for i in range(s1):
        for j in range(s2):
            
            ind = np.ravel_multi_index([[i],[j]],(s1,s2))[0]
            
            I_mult = [(i0,i1) for i0,i1 in itertools.product(range(i-1,i+2),range(j-1,j+2)) 
                 if i0>-1 and i0<s1 and i1>-1 and i1<s2 and (abs(i0-i)+abs(i1-j))<2 and
                 (abs(i0-i)+abs(i1-j))>0
                 ]
            
            I1 = [x[0] for x in I_mult]
            I2 = [x[1] for x in I_mult]
            
            I_lin = np.ravel_multi_index([I1,I2],(s1,s2))
                
            
            [G[ind].append((i,combined_risk[j[0],j[1]])) for i,j in zip(I_lin,I_mult)]



    path, weights = dijkstra(G, 0)

    print(weights[-1])

if __name__=='__main__':
    
    solve_problem1_2('test_input.txt')
    solve_problem1_2('input1.txt')
    
    solve_problem1_2('test_input.txt',True)
    solve_problem1_2('input1.txt',True)