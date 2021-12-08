#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def solve_problem2(input_path):
    
    with open(input_path,'r') as fp:
        
        lines = fp.readlines()

    lets = ['a','b','c','d','e','f','g']
    
    signal_dict = {
        '012345':0,
        '12':1,
        '01643':2,
        '01236':3,
        '1256':4,
        '02356':5,
        '023456':6,
        '012':7,
        '0123456':8,
        '012356':9
        }
    
    sum_val = 0
    
    for line in lines:
        segment_letters = ['' for i in range(7)]
    
        line = line.strip('\n')    
    
        lhs = line.split(' | ')[0].split(' ')
        
        lens = [len(x) for x in lhs]
        
        segment_letters[0] = list(set(lhs[lens.index(3)]).difference(lhs[lens.index(2)]))[0]
        
        union = set(lhs[lens.index(4)]).union(lhs[lens.index(3)])
        diffs = list([x for x in [set(x).difference(union) for i,x in zip(lens,lhs) if i==6] if len(x)==1][0])
        segment_letters[3] = diffs[0]
        
        union = set(lhs[lens.index(3)]).union([segment_letters[3],segment_letters[0]])
        diffs =   list([x for x in [set(x).difference(union) for i,x in zip(lens,lhs) if i==5] if len(x)==1][0])
        segment_letters[6] = diffs[0]
        
        union = set(lhs[lens.index(3)]).union([segment_letters[3],segment_letters[0],segment_letters[6]])
        diffs = list([x for x in [set(x).difference(union) for i,x in zip(lens,lhs) if i==6] if len(x)==1][0])
        segment_letters[5] = diffs[0]
        
        five = [x for x in lhs if segment_letters[5] in x and len(x)==5]
        segment_letters[2] = list(set(five[0]).difference(set(segment_letters)))[0]
        
        seven =  [x for x in lhs if len(x)==3]
        segment_letters[1] = list(set(seven[0]).difference(set(segment_letters)))[0]
        
        segment_letters[4] = list(set(lets).difference(set(segment_letters)))[0]
        
        rhs = line.split(' | ')[1].split(' ')
        result = ''
        
        for signal in rhs:
            signal_num = ''.join([str(segment_letters.index(x)) for x in signal])
            I = [signal_dict[x] for ind,x in enumerate(signal_dict.keys()) if set(x) == set(signal_num)][0]
            result += str(I)
        
        result = int(result)
        sum_val += result
        
    print(sum_val)
        

if __name__ == '__main__':
    
    solve_problem2('./test_input.txt')
    solve_problem2('./input1.txt')
