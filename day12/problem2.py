#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from adventofcode2021.utils import CaveGraph

def solve_problem2(input_path):
    with open(input_path,'r') as fp:
        
        lines = fp.readlines()
        
    graph = CaveGraph()
    
    for line in lines:
        line = line.strip('\n')
        node1 = line.split('-')[0]
        node2 = line.split('-')[1]
        
        if not graph.contains(node1):
            graph.add_node(node1)
    
            
        if not graph.contains(node2):
            graph.add_node(node2)
            
        graph.connect_nodes(node1,node2)
        
    paths = graph.find_all_paths('start', 'end')
    
    print(len(paths))

if __name__ == '__main__':
    
    solve_problem2('./test_input1.txt')
    solve_problem2('./test_input2.txt')
    solve_problem2('./test_input3.txt')
    solve_problem2('./input1.txt')
    
