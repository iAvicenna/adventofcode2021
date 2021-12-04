#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

from adventofcode2021 import utils

def solve_problem1(input_path):
    
    with open(input_path,'r') as fp:
        
        lines = fp.readlines()
        
    
    line_list = utils.split_list(lines, '\n')
    
    boards = np.zeros((len(line_list)-1,5,5))
    marks = np.zeros((len(line_list)-1,5,5))
    numbers = [int(x) for x in line_list[0][0].strip('\n').split(',')]
    
    for i0,lines in enumerate(line_list[1:]):
        board = np.zeros((5,5))
        
        for il,line in enumerate(lines):
            nums = [x for x in line.strip('\n').split(' ') if x!='']
            board[il,:] = nums
            
        boards[i0,:,:] = board
        
    board_ind = None
       
    for num in numbers:
        marks[boards==num] = 1
        
        mean_row = np.mean(marks,axis=1)
        mean_col = np.mean(marks,axis=2)
        
        if 1 in mean_row:
            inds = np.where(mean_row==1)
            if len(inds[0])>1:
                print('Multiple winning boards, taking first.')
            board_ind = inds[0][0]
        
        elif 1 in mean_col:
            inds = np.where(mean_col==1)
            if len(inds[0])>1:
                print('Multiple winning boards, taking first.')
            board_ind = inds[0][0]
    
        if board_ind is not None:
            board = boards[board_ind,:,:]
            board_marks = marks[board_ind,:,:]
            
            sum_val = np.sum(board[board_marks==0])
            
            print(sum_val*num)
            break
    
if __name__ == '__main__':
    solve_problem1('./test_input.txt')        
    solve_problem1('./input1.txt')        