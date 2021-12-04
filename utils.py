#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def split_list(lst, value):
    indices = [i for i, x in enumerate(lst) if x == value]
    split_list = []
    
    for i0,i1 in zip([-1, *indices], [*indices, len(lst)]):
        split_list.append(lst[i0+1:i1])
        
    return split_list

def binary_to_decimal(vec):
    
    return sum([vec[::-1][i]*2**i for i in range(len(vec))])