#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def solve_problem1(input_path):
    
    with open(input_path,'r') as fp:
    
        lines = fp.readlines()


    no_segments = [6,2,5,5,4,5,6,3,7,6]
    
    digits = [1,4,7,8]
    no_digit_segs = [no_segments[x] for x in digits]
    
    counter = 0
    
    for line in lines:
    
        line = line.strip('\n')    
    
        rhs = line.split(' | ')[1].split(' ')
        
        rhs_lens = [len(x) for x in rhs]
        
        counter += sum([rhs_lens.count(x) for x in no_digit_segs])
        
    print(counter)
    

if __name__ == '__main__':
    
    solve_problem1('./test_input.txt')
    solve_problem1('./input1.txt')
