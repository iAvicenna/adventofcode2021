#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from adventofcode2021.utils import ThermalPaper


def solve_problem2(input_path):
    
    paper = ThermalPaper()
    
    paper.read_input(input_path)
    
        
        
    paper.fold()
    
    print(np.count_nonzero(paper.locations))
        
    
            

if __name__ == '__main__':
    
    solve_problem2('./test_input.txt')
    solve_problem2('./input1.txt')
