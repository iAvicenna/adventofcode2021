#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from adventofcode2021.utils import OctopusGrid


def solve_problem2(input_path):
    octopus_grid = OctopusGrid()
    
    octopus_grid.read_input(input_path)
    
    
    for i in range(2000):
        octopus_grid.update()
        
        octopus_grid.print_flash()
        octopus_grid.print_energy()
        
        if all(x==0 for x in octopus_grid.energies.flatten()):
            
            print(f'Simultaneous flash at step {i+1}')
            break
            
        

if __name__ == '__main__':
    
     solve_problem2('./test_input1.txt')
     solve_problem2('./test_input2.txt')
     solve_problem2('./input1.txt')
