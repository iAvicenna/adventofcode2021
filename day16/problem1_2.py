#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from adventofcode2021.utils import binary_to_decimal as btd

repr_map ={
    'A':10,
    'B':11,
    'C':12,
    'D':13,
    'E':14,
    'F':15
    
    }

def hexa_to_binary(string):
    
    
    return ''.join(['0'*(4-len(bin(int(x)).replace('0b',''))) + bin(int(x)).replace('0b','') if 
                         x.isnumeric() else '0'*(4-len(bin(repr_map[x]).replace('0b',''))) 
                         + bin(repr_map[x]).replace('0b','') for x in string])

def sum_version(packets, depth=0):
    
    version_sum = 0
    
    if isinstance(packets[-1],list):
        for subpackets in packets[-1]:
            version_sum += sum_version(subpackets, depth+1)
    
    version_sum += packets[1]
    return version_sum
  
def compute(packets, depth=0):
    
    vals = []
    if isinstance(packets[-1],list):
        for subpackets in packets[-1]:
            val = compute(subpackets, depth+1)
            vals.append(val)
    else:
        vals = [packets[-1]]
    
    
    
    return packets[-2](vals)
      

def decode(string=None,hexa=None,depth=0):
    
    if string is not None:
        hexa = hexa_to_binary(string)
    else:
        assert hexa is not None, 'either supply string or hexa'
        
    packets = []
    
    while len(hexa)>0:
    
        version = btd(map(int,hexa[0:3]))
        id = btd(map(int,hexa[3:6]))
        
        if id==0:
            op = lambda x: sum(x)
            name = 'sum'
        elif id==1:
            op = lambda x: np.prod(x)
            name = 'prod'
        elif id==2:
            op = lambda x: min(x)
            name = 'min'
        elif id==3:
            op = lambda x: max(x)
            name = 'max'
        elif id==4:
            op = lambda x: x[0]
            name = 'literal'
        elif id==5:
            op = lambda x: int(x[0]>x[1])
            name = 'greater'
        elif id==6:
            op = lambda x: int(x[0]<x[1])
            name = 'less'
        elif id==7:
            op = lambda x: int(x[0]==x[1])
            name = 'equal'
            
            
        
        if id==4:
            
            num_hexa = []
            i=0
            stop = False
            
            while not stop:
                num_hexa += hexa[6+i*5+1:6+(i+1)*5]
                if hexa[6+i*5:6+(i+1)*5][0]=='0': stop=True
                i+=1
                
            num = btd([int(x) for x in num_hexa])

                
            hexa = hexa[6+i*5:]
            
            packets.append([name,version,id,op, num])
    
            if hexa.replace('0','')=='':
                hexa = ''
            
        else:
            
            length_id = btd(map(int,hexa[6:7]))
            subpackets = []
            
            
            if length_id == 0:
                subpacket_length = btd(map(int,hexa[7:22]))
                subpackets_hexa = hexa[22:22+subpacket_length]
                
                subpackets = decode(hexa=subpackets_hexa, depth=depth+1)
                
                packets.append([name,version,id,length_id,op,subpackets])
                
                hexa = hexa[22+subpacket_length:]
                
                if all(x=='0' for x in hexa):
                    hexa = ''
                
            elif length_id == 1:
                no_subpackets = btd(map(int,hexa[7:18]))
                
                subpackets = decode(hexa=hexa[18:], depth=depth+1)
                
                packets.append([name,version,id,no_subpackets,op,subpackets[0:no_subpackets]])
               
                if no_subpackets<len(subpackets):
                    packets += subpackets[no_subpackets:]
               
                hexa = ''
                
            else:
                raise ValueError(f'Invalid id {id} length_id {length_id} combination')
        
   
        
    return packets

if __name__ == '__main__':
    for i in range(1,8):
        print(f'test{i} ',end='')
        input_str = open(f'test_input{i}.txt','r').readlines()[0].strip('\n')
        packets = decode(input_str)
        
        if i>3:
            print(sum_version(packets[0]))
        else:
            print(packets)
        
    
    input_str = open('input1.txt','r').readlines()[0].strip('\n')
    packets = decode(input_str)
    print(f'Problem 1 ',end='')
    print(sum_version(packets[0]))
    
    for i in range(8,16):
        print(f'test{i} ',end='')
        input_str = open(f'test_input{i}.txt','r').readlines()[0].strip('\n')
        packets = decode(input_str)
        print(compute(packets[0]))
        
    input_str = open('input1.txt','r').readlines()[0].strip('\n')
    packets = decode(input_str)
    print('Problem 2 ',end='')
    print(compute(packets[0]))
