#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import itertools as it

class OctopusGrid():
    
    def __init__(self):
    
        self.energies = []
        self.shape = None
        self.adjacency_set = {}
        self.flash_count = 0
        
    def read_input(self, input_path):
        
        with open(input_path,'r') as fp:
            lines = fp.readlines()
        
        s1 = len(lines)
        
        energy_grid = [[] for i in range(s1)]
        
        
        for indline,line in enumerate(lines):
            energy_row = [int(x) for x in line.strip('\n')]
            
            energy_grid[indline] = energy_row
        
        self.energies = np.array(energy_grid, dtype=int)
        self.shape = self.energies.shape
        self._get_adjacency_set()
        
        
    def _get_adjacency_set(self):
        
        s1,s2 = self.shape
        
        for i in range(s1):
            for j in range(s2):
                
                self.adjacency_set[(i,j)] = []
                
                I = it.product(range(i-1,i+2),range(j-1,j+2))
        
                for i1,i2 in I:
                    if i1 in list(range(s1)) and i2 in list(range(s2)):
                        self.adjacency_set[(i,j)].append([i1,i2])
                        
                self.adjacency_set[(i,j)] = tuple(np.array(self.adjacency_set[(i,j)]).T.tolist())
    

    def update(self):
        
        s1,s2 = self.shape
        self._has_flashed = np.zeros(self.energies.shape, dtype=bool)
        self._has_charged = np.zeros(self.energies.shape, dtype=bool)
        
        self.energies +=1
        
    
        
        while 10 in self.energies:
            
            self.flash()
                
                
    def flash(self):
        
        s1,s2 = self.shape
        
        for i in range(s1):
            for j in range(s2):
                if self.energies[i,j]==10 and not self._has_flashed[i,j]:
        
                    self.flash_count += 1
                    self._has_flashed[i,j] = True
                    
                    x,y = self.adjacency_set[(i,j)]
                    I1 = []
                    I2 = []
                    
          
                    
                    for i1,i2 in zip(x,y):
                        if self.energies[i1,i2]!=10 and self.energies[i1,i2]!=0:
                            I1.append(i1)
                            I2.append(i2)
                    
                    self.energies[tuple([I1,I2])] += 1
                    self.energies[i,j] = 0
                    
                   
                    
                if self.energies[i,j]==10 and self._has_flashed[i,j]:
                    self.energies[i,j] = 9
                    
            
        
            
    def print_flash(self):

        s1,s2 = self.shape        
        return_str = ''

        for i in range(s1):
            for j in range(s2):
                if self._has_flashed[i,j]:
                    return_str += '*'
                else:
                    return_str += '.'
                    
            return_str += '\n'
        return_str += '\n'
        

        return return_str
        
    def print_energy(self):

        s1,s2 = self.shape        
        return_str = ''
        for i in range(s1):
            for j in range(s2):
                return_str += f'{self.energies[i,j]}'
            return_str += '\n'
        return_str += '\n'
        
        return return_str
            


class Graph():
    '''
    path finding algorithms is from https://www.python.org/doc/essays/graphs/
    others: Sina Tureli
    '''
    def __init__(self):
        self._node_map = {}
        self._number_of_nodes = 0
        self.adjacency_set = {}
        self.weights = {}

    def get_nodes(self):
        return list(self._node_map.keys())

    def add_node(self,node_name):

        if node_name not in self._node_map:
            self._node_map[node_name] = self._number_of_nodes
            self._number_of_nodes += 1
            self.adjacency_set[node_name] = []

    def connect_nodes(self, node_name1, node_name2, one_directional=False):

        assert node_name1 in self._node_map, f'{node_name1} not in graph'
        assert node_name2 in self._node_map, f'{node_name2} not in graph'


        if not one_directional and node_name1 not in self.adjacency_set[node_name2]:
            self.adjacency_set[node_name2].append(node_name1)
        if node_name2 not in self.adjacency_set[node_name1]:
            self.adjacency_set[node_name1].append(node_name2)

    def set_weight(self, node_name1, node_name2, weight):

        assert node_name2 in self.adjacency_set[node_name1], 'node_name2 is not in adjacency set of node_name1'

        self.weights[(node_name1, node_name2)] = weight

    def connected_component(self, node):
        
        prev_con_com = set([node])
        next_con_com = set()
        counter = 0
        while prev_con_com != next_con_com:
            
            if counter!=0:
                prev_con_com = next_con_com
            else:
                next_con_com = prev_con_com
            
            for a in prev_con_com:
                next_con_com = next_con_com.union(self.adjacency_set[a])
            
            counter += 1
            
            
        return next_con_com

    def find_shortest_path(self, start=None, end=None, path=[]):

            if start is None:
                start = self.entrance

            if end is None:
                end = self.exit

            graph = self.adjacency_set

            path = path + [start]
            if start == end:
                return path
            if not start in graph:
                return None
            shortest = None
            for node in graph[start]:
                if node not in path:
                    newpath = self.find_shortest_path(start=node, end=end, path=path)
                    if newpath:
                        if not shortest or len(newpath) < len(shortest):
                            shortest = newpath
            return shortest

    def find_path(self, start, end, path=[]):
        graph = self.adjacency_set
        path = path + [start]
        if start == end:
            return path
        if start not in graph:
            return None
        for node in graph[start]:
            if node not in path:
                newpath = self.find_path(node, end, path)
                if newpath: return newpath
        return None

    def find_all_paths(self, start, end, path=[]):
        path = path + [start]
        graph = self.adjacency_set

        if start == end:
            return [path]
        if start not in graph:
            return []
        paths = []

        for node in graph[start]:
            if node not in path:
                newpaths = self.find_all_paths(node, end, path)

                for newpath in newpaths:
                    paths.append(newpath)

        return paths


def split_list(lst, value):
    indices = [i for i, x in enumerate(lst) if x == value]
    split_list = []
    
    for i0,i1 in zip([-1, *indices], [*indices, len(lst)]):
        split_list.append(lst[i0+1:i1])
        
    return split_list

def binary_to_decimal(vec):
    
    return sum([vec[::-1][i]*2**i for i in range(len(vec))])