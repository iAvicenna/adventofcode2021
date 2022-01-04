#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import itertools as it
from adventofcode2021.utils import QuantumDiceGameUniverse

circular = [10, 1,2,3,4,5,6,7,8,9]

def generate_ends(start):
    
    '''
    Given a starting number this generated all the possible end 
    end points by rolling three dices with faces 1,2,3 and counts the number
    of combinations of dice rools that ends there. Note that numbers are circular
    i.e 10 = 0, 11=1 etc...
    '''
    
    end_points = []
    
    for a,b,c in it.product(range(1,4),range(1,4), range(1,4)):
        
        end = circular[(start + a + b + c)%10]
        
        end_points.append(end)
        
    end_set = sorted(list(set(end_points)))
    
    end_dict = {x:end_points.count(x) for x in end_set}
    
    return end_dict
        

def solve_problem2(input_path, score_threshold=21):
    
    input_lines = list(map(str.rstrip,open(input_path,'r')))
    
    start1 = int(input_lines[0].split(': ')[-1])
    start2 = int(input_lines[1].split(': ')[-1])
        
    qdt1 = QuantumDiceGameUniverse(start1, score_threshold)
    qdt2 = QuantumDiceGameUniverse(start2, score_threshold)
    
    '''
    QuantumDiceGameUniverse builds the distribution of number of paths that
    either pass or do not pass the score threshold after n throws of the quantum
    dice. Its inputs are the starting number for each player and the score threshold
    that you need to pass in order to win the game.
    '''
    
    level = 0
    generated_ends = {}
    
    for start in range(1,11):
        end_dict = generate_ends(int(start))
        generated_ends[str(start)] = end_dict
    
    
    while len(qdt1.path_levels[level])>0:
        
        for node_name in qdt1.path_levels[level]:
            
            start = node_name.split(';')[0]
           
            end_dict = generated_ends[start]
            
            for key in end_dict:
                
                val = end_dict[key]
                
                qdt1.add_node(f'{key};{node_name}', val, level+1, node_name)
    
        level += 1
             
    level = 0
    
    while len(qdt2.path_levels[level])>0:
        
        for node_name in qdt2.path_levels[level]:
            
            start = node_name.split(';')[0]
           
            end_dict = generated_ends[start]
            
            for key in end_dict:
                
                val = end_dict[key]
                
                qdt2.add_node(f'{key};{node_name}', val, level+1, node_name)
    
        level += 1
             
    
    distribution1 = qdt1.level_winning_distribution()
    
    sum_win = 0
    
    for i in range(1,len(distribution1)):
        
        sum_win += distribution1[i]*qdt2.paths_per_level[i]/27  # the normalization is for the fact that
                                                                # if we look at number of paths for which
                                                                # player 1 wins at turn n and multiply
                                                                # it by the number of paths player 2 does not
                                                                # win at turn n, there is a redundant evolution of
                                                                # player 2 paths from its turn at n-1 to n 
        
    return int(sum_win)


if __name__=='__main__':
    
    
     test_result = solve_problem2('test_input1.txt')
     
     assert test_result == 444356092776315
     
     result = solve_problem2('input1.txt')

     print(f'Number of times player 1 wins: {result}')
     
     assert result == 221109915584112
    
    