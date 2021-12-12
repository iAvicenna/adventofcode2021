#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from adventofcode2021.utils import Graph


def solve_problem1(input_path):
    
    with open(input_path,'r') as fp:
        
        lines = fp.readlines()
        
    graph = Graph()
    
    for line in lines:
        line = line.strip('\n')
        node1 = line.split('-')[0]
        node2 = line.split('-')[1]
        
        if not graph.contains(node1):
            if node1 not in ['start','end'] and not node1.islower():
                graph.add_node(node1, max_visits=np.inf)
            elif not graph.contains(node1):
                graph.add_node(node1, max_visits=1)
    
            
        if not graph.contains(node2):
            if node2 not in ['start','end'] and not node2.islower():
                graph.add_node(node2, max_visits=np.inf)
            elif not graph.contains(node2):
                graph.add_node(node2, max_visits=1)
            
        
            
        graph.connect_nodes(node1,node2)
        
    paths = graph.find_all_paths('start', 'end')
    
    print(len(paths))


if __name__ == '__main__':
    
    solve_problem1('./test_input1.txt')
    solve_problem1('./test_input2.txt')
    solve_problem1('./test_input3.txt')
    solve_problem1('./input1.txt')
