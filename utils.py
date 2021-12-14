#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import itertools as it


def split_list(lst, value):
    indices = [i for i, x in enumerate(lst) if x == value]
    split_list = []
    
    for i0,i1 in zip([-1, *indices], [*indices, len(lst)]):
        split_list.append(lst[i0+1:i1])
        
    return split_list

def binary_to_decimal(vec):
    
    return sum([vec[::-1][i]*2**i for i in range(len(vec))])

class Polymer():
    
    def __init__(self, template, polymerization_dictionary):
        
        self.template = template
        self.polymerization_dictionary = polymerization_dictionary
        self.alphabet = list(self.polymerization_dictionary.values())
        self.letter_count = {x:self.template.count(x) for x in self.alphabet}
        self.current = {x:self.template.count(x) for x in self.polymerization_dictionary.keys()}
        
    def polymerize(self):
        
        letter_count = {x:0 for x in self.alphabet}
        new_polymer = {x:0 for x in self.polymerization_dictionary.keys()}
        
        
        for dimer in self.current:
            if self.current[dimer]>0:
                count = self.current[dimer]
                self.current[dimer] = 0
                
                new_dimer1 = dimer[0] + self.polymerization_dictionary[dimer]
                new_dimer2 = self.polymerization_dictionary[dimer] + dimer[1]
                
                
                new_polymer[new_dimer1] += count
                new_polymer[new_dimer2] += count
                
                letter_count[new_dimer1[0]] += count
                letter_count[new_dimer1[1]] += count # second letter of dimer2 
                                                     # will be counted as the first letter 
                                                     # of another dimer except terminal
                                                     # which is added at the end
                                              
                
        letter_count[self.template[-1]] += 1
                                               
        self.letter_count = letter_count
        self.current = new_polymer

    def score(self):
        
        return max(list(self.letter_count.values())) - min(list(self.letter_count.values()))

    def __repr__(self):
        
        return self.current

class ThermalPaper():
    
    def __init__(self):
        
        self.locations = []
        self.folds = []
        
    def read_input(self, input_path):
        
        with open(input_path,'r') as fp:
            lines = fp.readlines()
        
        split_input = split_list(lines,'\n')
        coord_lines = split_input[0]
        fold_lines = split_input[1]
        
        coordsx = []
        coordsy = []
        maxx = 0
        maxy = 0
        for line in coord_lines:
            line = line.strip('\n')
            x = int(line.split(',')[0])
            y = int(line.split(',')[1])
            
            maxx = max([x,maxx])
            maxy = max([y,maxy])
            
            coordsx.append(x)
            coordsy.append(y)
            
        s2 = maxx+1
        s1 = maxy+1
        
        for fold in fold_lines:
            fold = fold.strip('\n')
            fold = fold.split(' ')[-1]
            self.folds.append(fold)
        
        self.locations = np.zeros((s1,s2),dtype=bool)
        self.locations[tuple([coordsy,coordsx])]=True
        
    def fold(self):
        
        if len(self.folds)>0:
            fold = self.folds[0]
            self.folds = self.folds[1:]
            coord = int(fold.split('=')[-1])
            
            if 'x' in fold:
                
                part1 = self.locations[:,:coord][:,::-1]
                part2 = self.locations[:,coord+1:]
                
                _,s1 = part1.shape
                _,s2 = part2.shape
                
                s3 = min(s1,s2)
                
                if s1>s2:
                    new_array = part1.copy()
                else:
                    new_array = part2.copy()     
                
                or_array = np.logical_or(part1[:,:s3],part2[:,:s3])
                
                new_array[:,:s3] = or_array
                
            elif 'y' in fold:
                
                part1 = self.locations[:coord,:][::-1,:]
                part2 = self.locations[coord+1:,:]
                
                s1,_ = part1.shape
                s2,_ = part2.shape
                
                s3 = min(s1,s2)
                
                if s1>s2:
                    new_array = part1.copy()
                else:
                    new_array = part2.copy()  
                
                or_array = np.logical_or(part1[:s3,:],part2[:s3,:])
                
                new_array[:s3,:] = or_array
                
            self.locations = new_array
        else:
            print('Cant fold anymore')
      
    def print(self):
        
        s1,s2 = self.locations.shape
        return_str = ''
        for i in range(s1):
            for j in range(s2):
                if self.locations[i,j]:
                    return_str += '#'
                else:
                    return_str += '.'
            return_str += '\n'
            
        return_str += '\n'
        
        return return_str

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
        self.max_visits = {}

    def get_nodes(self):
        return list(self._node_map.keys())

    def add_node(self,node_name, max_visits):

        if node_name not in self._node_map:
            self._node_map[node_name] = self._number_of_nodes
            self._number_of_nodes += 1
            self.adjacency_set[node_name] = []
            self.max_visits[node_name] = max_visits

    def contains(self,node_name):
        
        return node_name in self._node_map

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
            if path.count(node) < self.max_visits[node]:
                newpaths = self.find_all_paths(node, end, path)

                for newpath in newpaths:
                    paths.append(newpath)

        return paths



class CaveGraph():
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

    def contains(self,node_name):
        
        return node_name in self._node_map

    def connect_nodes(self, node_name1, node_name2, one_directional=False):

        assert node_name1 in self._node_map, f'{node_name1} not in graph'
        assert node_name2 in self._node_map, f'{node_name2} not in graph'


        if not one_directional and node_name1 not in self.adjacency_set[node_name2]:
            self.adjacency_set[node_name2].append(node_name1)
        if node_name2 not in self.adjacency_set[node_name1]:
            self.adjacency_set[node_name1].append(node_name2)


    def find_all_paths(self, start, end, path=[]):
        path = path + [start]
        graph = self.adjacency_set

        if start == end:
            return [path]
        if start not in graph:
            return []
        paths = []

        for node in graph[start]:

            small_caves = [x for x in path if x.islower()]
            if ((node in ['start','end'] and path.count(node)<1) or
                node.isupper() or
                (node not in ['start','end'] and node.islower() and path.count(node)<2 and len(small_caves) == len(set(small_caves))) or
                (node not in ['start','end'] and node.islower() and path.count(node)<1)
                ):
                newpaths = self.find_all_paths(node, end, path)

                for newpath in newpaths:
                    paths.append(newpath)

        return paths

