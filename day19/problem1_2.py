#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import itertools as it
from scipy.spatial import distance
from adventofcode2021.utils import split_list, Graph


def solve_problem1_2(input_path):
    
    
    common_number_of_beacons = 12
    
    lines = list(map(str.strip,open(input_path,'r').readlines()))
    
    scanner_outputs = split_list(lines, '')
    
    beacon_rel_coordinates = []
    
    for output in scanner_outputs:
        
        dim = len(output[1].split(','))
        
        beacon_rel_coordinates.append(np.zeros((len(output)-1,dim),dtype=int))
        
        for ind,coords in enumerate(output[1:]):
            
            beacon_rel_coordinates[-1][ind,:] = [int(x) for x in coords.split(',')]
            
    
    s1,s2 = beacon_rel_coordinates[0].shape
    transformations = []
    dim = s2


    '''
    generate all possible transformations of the scanners
    '''    
    if dim == 3:
       
        I = it.permutations(range(3))
        
        for i0,i1,i2 in I:
            for dir0,dir1,dir2 in list(it.product([-1,1],[-1,1],[-1,1])):
                
                M = np.zeros((dim,dim),dtype=int)
                M[0,i0] = dir0
                M[1,i1] = dir1
                M[2,i2] = dir2
                
                if np.linalg.det(M)==1:
                    transformations.append(M)
                 
    elif dim == 2:
        for xdir in [1,-1]:
            for ydir in [1,-1]:
                M = np.array([[xdir,0],[0,ydir]],dtype=int)
                transformations.append(M)
            
            
    found_scanner_pairs = []
    scanner_transformations = {}
    scanner_adjacency = []
    nbeacons = len(beacon_rel_coordinates)
    
    '''
    for a given set of positions with respect to a scanner,
    generate all transformed positions with respect to the 
    given transformations above. Then for any other scanner
    we check whether if there are 12 beacon coordinates which
    overlap with any of the transformed coordinates, we keep
    a record of it. We also form a graph in which every node
    is a scanner and two scanners are connected if they share
    12 beacons. In this way by finding the path from scanner 0
    to any scanner on this graph, we can compose transformations
    and apply this transformation to (0,0,0) i,e coordinate of scanner 0
    to get coordinate of other scanners so one can compute the
    maximum distance in the second problem.
    '''
    
    for bind0,coordinates0 in enumerate(beacon_rel_coordinates):
        
        extended_coordinates0 = np.zeros((*coordinates0.shape,len(transformations)),dtype=int)
        scanner_adjacency.append([])
    
        for i in range(len(transformations)):
            extended_coordinates0[:,:,i] = (transformations[i]@coordinates0.T).T
            
        
            
        for bind1,coordinates1 in enumerate(beacon_rel_coordinates[bind0+1:],start=bind0+1):
            
            
            if sorted([bind0,bind1]) not in found_scanner_pairs:
                
                pair_map = {}
                
                
                for i in range(len(transformations)):
                    
                    s1 = coordinates0.shape[0]
                    s2 = coordinates1.shape[0]
                    M = []
                    
     
                    for i0,i1 in it.product(range(s1),range(s2)):
                        M.append(str(list(extended_coordinates0[i0,:,i] - coordinates1[i1,:])))
                            
                    Mset = list(set(M))
                    
                    counts = [M.count(m) for m in Mset]
                    max_counts = max(counts)
                    
                    
                    if max_counts == common_number_of_beacons:
    
                        ind = np.argmax(counts)
                        shift = Mset[ind]
                        
                        if dim==2:
                            shift = [float(shift.split(',')[0][1:]),float(shift.split(',')[1][:-1])]
                        elif dim==3:
                            shift = [float(shift.split(',')[0][1:]),float(shift.split(',')[1]),float(shift.split(',')[2][:-1])]
                        
                        shift = np.reshape(np.array(shift,dtype=int),(3,1))
                        shift = np.tile(shift,(1,coordinates1.shape[0])).T
                        new_coordinates1 = coordinates1 + shift
                        
                        for j in range(s2):
    
                            J = [ind for ind in range(s1) if np.linalg.norm(new_coordinates1[j,:] - extended_coordinates0[ind,:,i])<1e-8]
                            if len(J)>0:
                                pair_map[j]=J[0]
                                
                        found_scanner_pairs.append(sorted([bind0,bind1]))
               
                        scanner_adjacency[-1].append(bind1)
                       
                        inv_shift = (np.linalg.inv(transformations[i])@shift.T).T
                       
                        scanner_transformations[(bind0,bind1)] = (transformations[i], shift[0,:]) 
                        scanner_transformations[(bind1,bind0)] = (np.linalg.inv(transformations[i]), -inv_shift[0,:]) 
                       
                        break
                                    
                        
                            
    scanner_graph = Graph()
    [scanner_graph.add_node(i) for i in range(nbeacons)]
    [scanner_graph.connect_nodes(i,j) for i in range(nbeacons) for j in scanner_adjacency[i]]
    all_coordinates = []
    all_scanner_coordinates = [[0,0,0]]
    
    for coord in list(beacon_rel_coordinates[0]):
        
        if str(coord) not in all_coordinates:
             all_coordinates.append(str(coord))
    
    
    for i in range(1,nbeacons):
        p = scanner_graph.find_path(0, i)
        coordinates = beacon_rel_coordinates[i]
        scanner_coordinates = [0,0,0]
        
        if p is not None:
            for i in range(len(p)-1,0,-1):
                p1 = p[i]
                p0 = p[i-1]
                
                T,S = scanner_transformations[(p0,p1)]
                
                coordinates = coordinates + S
                
                coordinates = (np.linalg.inv(T)@coordinates.T).T
                
                coordinates = coordinates.astype(int)
                
                scanner_coordinates = scanner_coordinates + S
                scanner_coordinates = (np.linalg.inv(T)@scanner_coordinates.T).T
                
                
            all_scanner_coordinates.append(scanner_coordinates)
            
            for coord in list(coordinates):
                
                if str(coord) not in all_coordinates:
                     all_coordinates.append(str(coord))
        
        
        
        
        
    dist = distance.pdist(np.array(all_scanner_coordinates),'cityblock')    
    
    return len(all_coordinates), int(np.max(dist))
    

if __name__ == '__main__':
    
    no, dist = solve_problem1_2('test_input1.txt')
    
    assert no==79 and dist==3621

    #takes about a minute on intel core i7
    no, dist = solve_problem1_2('input1.txt')

    print(f'Number of beacons is {no}')
    print(f'Max distance is {dist}')     
    
    assert no==394 and dist==12304
    
    