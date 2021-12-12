#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from adventofcode2021.utils import OctopusGrid


def solve_problem1(input_path):
    octopus_grid = OctopusGrid()
    
    octopus_grid.read_input(input_path)
    
    
    for i in range(100):
        octopus_grid.update()
        
        octopus_grid.print_flash()
        octopus_grid.print_energy()
        
        
        if i+1==100:    
            print(octopus_grid.flash_count)

if __name__ == '__main__':
    
     solve_problem1('./test_input1.txt')
     solve_problem1('./test_input2.txt')
     solve_problem1('./input1.txt')
