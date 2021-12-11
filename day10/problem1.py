#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

score = {
 ')':3,
 ']':57,
 '}':1197,
 '>':25137
 }

mistakes = []
for line in lines:
    line = line.strip('\n')
    
    opens=[]
    
    
    for let in line:
        if let in open_list:
            opens.append(let)
        if let in close_list:
            if opens[-1] == invert[let]:
                opens.pop(len(opens)-1)
            else:
                mistakes.append(let)
                break
                
print(sum([score[x] for x in mistakes]))
    

# if __name__ == '__main__':
    
#     #solve_problem1('./test_input.txt')
#     #solve_problem1('./input1.txt')
