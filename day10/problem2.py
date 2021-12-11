#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
input_path = 'input1.txt'
with open(input_path,'r') as fp:
    
    lines = fp.readlines()
        
open_list = ['(','[','{','<']    
close_list = [')',']','}','>']
invert = {
 ')':'(',
 ']':'[',
 '}':'{',
 '>':'<'
 }
forward = {
    '(':')',
    '[':']',
    '{':'}',
    '<':'>'
    
    }

score_map = {
 ')':1,
 ']':2,
 '}':3,
 '>':4
 }

mistakes = []

autocomplete = []
for ind,line in enumerate(lines):
    line = line.strip('\n')
    
    opens=[]
    discard = False
    
    for let in line:
        if let in open_list:
            opens.append(let)
        if let in close_list:
            if opens[-1] == invert[let]:
                opens.pop(len(opens)-1)
            else:
                mistakes.append(let)
                discard = True
                break
            
    if not discard:
        autocomplete.append([forward[x] for x in opens[::-1]])

scores = []
for completion in autocomplete:
    score = 0
    for elem in completion:
        score = 5*score + score_map[elem]
    scores.append(score)
    

scores = np.sort(scores)
s = scores.size
print(scores[int((s-1)/2)])


# if __name__ == '__main__':
    
#     #solve_problem1('./test_input.txt')
#     #solve_problem1('./input1.txt')
