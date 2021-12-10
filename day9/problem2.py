#!/usr/bin/env python3
# -*- coding: utf-8 -*-

input_path = 'input1.txt'
import numpy as np
from adventofcode2021.utils import Graph

def solve_problem2(input_path):  
    with open(input_path,'r') as fp:
        lines = fp.readlines()
        
     
    s1 = len(lines)
    s2 = len(lines[0].strip('\n'))
    
    height_map = 10*np.ones((s1+2,s2+2))
    
    
    for ind,line in enumerate(lines):
        height_map[ind+1,1:s2+1] = [int(x) for x in line.strip('\n')]
        
    is_low = np.zeros((s1,s2),dtype=bool)
    filter_M = np.array([[False,True,False],[True,False,True],[False,True,False]])
    for i0 in range(1,s1+1):
        for i1 in range(1,s2+1):
            val = height_map[i0,i1]
    
            is_low[i0-1,i1-1] = all(val<x for x in height_map[i0-1:i0+2,i1-1:i1+2][filter_M])
            
     
    minima = [np.ravel_multi_index(x,(s1,s2)) for x in np.argwhere(is_low==1)]
    
    peaks = np.zeros((s1,s2), dtype=bool)
    peaks[height_map[1:s1+1,1:s2+1]==9]=True
    peaks = peaks.flatten()
    
    map_graph = Graph()
    [map_graph.add_node(i) for i in range(s1*s2)]
    [map_graph.connect_nodes(i,i+1) for i in range(s1*s2-1) if i%s2!=s2-1 and not peaks[i] and not peaks[i+1]]
    [map_graph.connect_nodes(i,i-1) for i in range(1,s1*s2) if i%s2!=0 and not peaks[i] and not peaks[i-1]]
    [map_graph.connect_nodes(i,i+s2) for i in range(s1*s2-s2) if not peaks[i] and not peaks[i+s2]] 
    [map_graph.connect_nodes(i,i-s2) for i in range(s2,s1*s2) if not peaks[i] and not peaks[i-s2]]
    
    connected_components = []
    
    [connected_components.append(map_graph.connected_component(m)) for m in minima]
    
    lengths = [len(x) for x in connected_components]
    
    print(np.prod(np.sort(lengths)[::-1][0:3]))
    

if __name__ == '__main__':
    
    solve_problem2('./test_input.txt')
    solve_problem2('./input1.txt')
