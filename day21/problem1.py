#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def solve_problem1(input_path):
    
    input_lines = list(map(str.rstrip,open(input_path,'r')))
    
    pos1 = input_lines[0].split(': ')[-1]
    pos2 = input_lines[1].split(': ')[-1]
    
    dice = 1
    
    players = [int(pos1),int(pos2)]
    scores = [0,0]
    
    counter= 0 
    circular = [10, 1,2,3,4,5,6,7,8,9]
    nrolled = 0
    while max(scores)<1000:
        
        if dice==101:
            dice = 1
        
        rolled_sum = sum(range(dice,dice+3))
        
        players[counter%2] += rolled_sum
            
        scores[counter%2] += circular[players[counter%2]%10]
        
        dice = dice + 3
        nrolled += 3
       
            
        counter +=1
        
    return min(scores)*nrolled
    

if __name__ == '__main__':
    
    test_result = solve_problem1('test_input1.txt')
    
    assert test_result == 739785
    
    result = solve_problem1('input1.txt')
    
    print(f'Result is {result}')
    
    assert result == 752247