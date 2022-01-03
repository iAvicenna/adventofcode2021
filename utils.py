#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import itertools as it
import heapq as hq
import math
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random 
import time

from timeit import default_timer as timer
from anytree import Node, RenderTree


class Interval():
    
    def __init__(self,a0=None,a1=None):
        
        '''
        Interval arithmetic where single points count as
        intervals of length 1 and generalizes trivially.
        Empty interval are initialized as -np.inf,-np.inf
        '''
        
        if a0 != None and a1 != None:
            
            if a0<=a1:
                self.a0 = a0
                self.a1 = a1
            else:
                self.a0 = -np.inf
                self.a1 = -np.inf
                
     
        else:
            self.a0 = -np.inf
            self.a1 = -np.inf
        
    def contains(self, interval):
        
        return self.a0 <= interval.a0 and self.a1 >= interval.a1
    
    def intersects(self, interval):
        
        return not(self.a1<interval.a0 or self.a0>interval.a1)
    
    def intersection(self, interval):
        
        if self.a1<interval.a0 or self.a0>interval.a1:
            return Interval()
        else:
            return Interval(max(min(self.a0,interval.a1),interval.a0),min(max(self.a1,interval.a0),interval.a1))
    
    def difference(self, interval):
        
        if not self.intersects(interval):
            
            return self
        
        elif self.contains(interval):
            
            I0 = Interval(self.a0,interval.a0-1)
            I1 = Interval(interval.a1+1, self.a1)
            
            I = []
            
            if I0.len()>0:
                I.append(I0)
            if I1.len()>0:
                I.append(I1)
                
            return I
            
        elif interval.contains(self):
            
            return []
        
        elif interval.a1 > self.a1:
            
            return [Interval(self.a0, interval.a0-1)]
        
        elif interval.a0 < self.a0:
            
            return [Interval(self.a0, interval.a1-1)]
        
    
    def complement(self):
        
        complement = []
        
        if np.isinf(self.a0) and np.isinf(self.a1): 
            if self.a1>self.a0:
                return [Interval([])]
            else:
                return [Interval(-np.inf, np.inf)]
        
        if not np.isinf(self.a0):
            complement.append(Interval(-np.inf,self.a0-1))
            
        if not np.isinf(self.a1):
            complement.append(Interval(self.a1+1,np.inf))
    
        return complement


    def complement_intersection(self, interval):
        
        if not self.intersects(interval):
            
            return [interval]
        
        else:
            
            complement = self.complement()
            
            I = [x.intersection(interval) for x in complement]
            I = [x for x in I if not x.is_empty()]
            
            return I
    
    def len(self):
        
        if np.isinf(self.a0) and np.isinf(self.a1) and np.sign(self.a0)==np.sign(self.a1):
            return 0 
        else:
            return self.a1 - self.a0 + 1
    
    def is_empty(self):
        
        return self.len() == 0
    
    def __repr__(self):
        
        return str([self.a0,self.a1])



class Cube():
    
    def __init__(self,Ix=None,Iy=None,Iz=None):
        
        if Ix is not None and Iy is not None and Iz is not None:
            self.Ix = Ix
            self.Iy = Iy
            self.Iz = Iz
            
        else:
            self.Ix = Interval()
            self.Iy = Interval()
            self.Iz = Interval()
        
    def intersects(self, cube):
        
        return (self.Ix.intersects(cube.Ix) and 
                self.Iy.intersects(cube.Iy) and 
                self.Iz.intersects(cube.Iz))
    
    def intersection(self, cube):
        
        iIx  = self.Ix.intersection(cube.Ix)
        iIy  = self.Iy.intersection(cube.Iy)
        iIz  = self.Iz.intersection(cube.Iz)
        
        
        if iIx.len == 0 or iIy.len == 0 or iIz.len == 0:

            return Cube(Interval(),Interval(),Interval())
        
        else:
            
            return Cube(iIx,iIy,iIz)
            
    def contains(self, cube):
        
        return (self.Ix.contains(cube.Ix) and
                self.Iy.contains(cube.Iy) and
                self.Iz.contains(cube.Iz))
    
    def complement(self):
        
        cIx = [self.Ix] + self.Ix.complement()
        cIy = [self.Iy] + self.Iy.complement()
        cIz = [self.Iz] + self.Iz.complement()
        
        if len(cIx) == 0 or len(cIy) == 0 or len(cIz) == 0:
        
            return [Cube()]
        
        else:
            complement = []
            
            for i0 in range(len(cIx)):
                for i1 in range(len(cIy)):
                    for i2 in range(len(cIz)):
                        
                        if ((i0 != 0 or i1 != 0 or i2 !=0) and 
                            cIx[i0].len()>0 and cIy[i1].len()>0 and cIz[i2].len()>0):
                            complement.append(Cube(cIx[i0],cIy[i1],cIz[i2]))

            return complement

    def complement_intersection(self, cube0):
        
        if not self.intersects(cube0):
            return cube0
        
        else:
            parts = []
            
            for cube1 in self.complement():
            
                if cube1.intersects(cube0):
                    parts.append(cube1.intersection(cube0))
                
            return parts

    def vol(self):
        
        return self.Ix.len()*self.Iy.len()*self.Iz.len()
    
    def difference(self, cube0):
        
        
        if not self.intersects(cube0):
            return [self]
        elif cube0.contains(self):
            return [Cube()]
        else:
            
            intersection = self.intersection(cube0)
            return intersection.complement_intersection(self)
    
    def plot(self):
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
    
        xlims,ylims,zlims = [self.Ix.a0,self.Ix.a1],  [self.Iy.a0,self.Iy.a1],  [self.Iz.a0,self.Iz.a1]
        
        voxelarray = np.zeros((xlims[1]-xlims[0]+1, ylims[1]-ylims[0]+1, zlims[1]-zlims[0]+1))
        voxelcolors = np.empty(voxelarray.shape,dtype=object)
        
        
        Ix = [self.cube.Ix.a0, self.cube.Ix.a1]
        Iy = [self.cube.Iy.a0, self.cube.Iy.a1]
        Iz = [self.cube.Iz.a0, self.cube.Iz.a1]
        
        if np.isinf(Ix[0]):
            Ix[0] = xlims[0]
        if np.isinf(Ix[1]):
            Ix[1] = xlims[1]
            
        if np.isinf(Iy[0]):
            Iy[0] = ylims[0]
        if np.isinf(Iy[1]):
            Iy[1] = ylims[1]
        
        if np.isinf(Iz[0]):
            Iz[0] = zlims[0]
        if np.isinf(Iz[1]):
            Iz[1] = zlims[1]
            
        Ix = [Ix[0]-xlims[0], Ix[1]-xlims[0]]
        Iy = [Iy[0]-ylims[0], Iy[1]-ylims[0]]
        Iz = [Iz[0]-zlims[0], Iz[1]-zlims[0]]
        
        Ix = list(range(Ix[0],Ix[1]+1))
        Iy = list(range(Iy[0],Iy[1]+1))
        Iz = list(range(Iz[0],Iz[1]+1))
        
        I = tuple(np.array(list(it.product(Ix,Iy,Iz))).T)

        voxelarray[I] = True

        ax.voxels(voxelarray, edgecolor='k', facecolors=voxelcolors)

    def __repr__(self):
        
        return f'<{self.Ix},{self.Iy},{self.Iz}>'

class Cuboid():
    
    def __init__(self, cubes=None):
        
        self.cubes = []
        
        if cubes is not None:
            self.add_cubes(cubes)
        
    def add_cubes(self,cubes0, depth=0):
        
        for ind0,cube0 in enumerate(cubes0):
                  
            if self.contains(cube0):
                continue
            
            elif not self.intersects(cube0):
                self.cubes.append(cube0)
                
            else:
                
                if depth == 0:
                    I = [ind for ind,cube1 in enumerate(self.cubes) if cube0.contains(cube1)]
                    
                    if len(I)>0:
                        self.remove_cubes(I)
  
                if cube0.vol()>0:
                    
                    if len(self.cubes)==0:
                        self.cubes = [cube0]
                    else:
                        for cube1 in self.cubes:
                            
                            if cube1.intersects(cube0):
                                
                                parts = cube1.complement_intersection(cube0)
                                
                                self.add_cubes(parts,depth+1)
                                                            
                                break
    
    def remove_cubes(self,inds):
        
        I = [x for x in range(len(self.cubes)) if x not in inds]
        self.cubes = [self.cubes[x] for x in I]
    
    def difference(self,cube0):
        
        if len(self.cubes)==0:
            return self
        
        remove_cube_inds = []
        cubes_to_add = []
        
        for ind1,cube1 in enumerate(self.cubes):
            
            if not cube1.intersects(cube0):
                continue
            
            else:
                cubes_to_add += [x for x in cube1.difference(cube0) if x.vol()>0]
                remove_cube_inds.append(ind1)
                
        self.remove_cubes(remove_cube_inds)
        
        self.add_cubes(cubes_to_add)
                    
                
    def intersects(self, cube0):
        
        if len(self.cubes)==0:
            return False
        
        for cube1 in self.cubes:
            
            if cube1.intersects(cube0):
                return True
            
        return False
    
    
    def contains(self, cube0):
        
        for cube in self.cubes:
            
            if cube.contains(cube0):
                return True
            
        return False

    def limits(self, universe_lim=100, buf=10):
        
        ul = universe_lim 
        
        x=[np.inf,-np.inf]
        y=[np.inf,-np.inf]
        z=[np.inf,-np.inf]
        
        for cube in self.cubes:
            
            x[0] = min(cube.Ix.a0,x[0])
            x[1] = max(cube.Ix.a1,x[1])
            
            y[0] = min(cube.Iy.a0,y[0])
            y[1] = max(cube.Iy.a1,y[1])
            
            z[0] = min(cube.Iz.a0,z[0])
            z[1] = max(cube.Iz.a1,z[1])
            
        if np.isinf(x[0]): x[0]=-ul
        if np.isinf(x[1]): x[1]=-ul
        if np.isinf(y[0]): y[0]=-ul
        if np.isinf(y[1]): y[1]=-ul
        if np.isinf(z[0]): z[0]=-ul
        if np.isinf(z[1]): z[1]=-ul
            
        if x[1]-x[0]>2*ul:
            
            cx = int(x[1]-x[0])/2
            x = [cx-ul, cx+ul]
            
            cy = int(y[1]-y[0])/2
            y = [cy-ul, cy+ul]
            
            cz = int(z[1]-z[0])/2
            z = [cz-ul, cz+ul]
            
        x = [x[0]-buf, x[1]+buf]
        y = [y[0]-buf, y[1]+buf]
        z = [z[0]-buf, z[1]+buf]
            
        return x, y, z
            

    def plot(self):
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
    
        xlims,ylims,zlims = self.limits()
        
        voxelarray = np.zeros((xlims[1]-xlims[0]+1, ylims[1]-ylims[0]+1, zlims[1]-zlims[0]+1))
        voxelcolors = np.empty(voxelarray.shape,dtype=object)
        
        colors = list(mcolors.TABLEAU_COLORS)
        random.shuffle(colors)
        
        
        for ind,cube in enumerate(self.cubes):
            
            if cube.vol()>0:
            
                Ix = [cube.Ix.a0, cube.Ix.a1]
                Iy = [cube.Iy.a0, cube.Iy.a1]
                Iz = [cube.Iz.a0, cube.Iz.a1]
                
                if np.isinf(Ix[0]):
                    Ix[0] = xlims[0]
                if np.isinf(Ix[1]):
                    Ix[1] = xlims[1]
                    
                if np.isinf(Iy[0]):
                    Iy[0] = ylims[0]
                if np.isinf(Iy[1]):
                    Iy[1] = ylims[1]
                
                if np.isinf(Iz[0]):
                    Iz[0] = zlims[0]
                if np.isinf(Iz[1]):
                    Iz[1] = zlims[1]
                    
                Ix = [Ix[0]-xlims[0], Ix[1]-xlims[0]]
                Iy = [Iy[0]-ylims[0], Iy[1]-ylims[0]]
                Iz = [Iz[0]-zlims[0], Iz[1]-zlims[0]]
                
                Ix = list(range(Ix[0],Ix[1]+1))
                Iy = list(range(Iy[0],Iy[1]+1))
                Iz = list(range(Iz[0],Iz[1]+1))
                
                I = tuple(np.array(list(it.product(Ix,Iy,Iz))).T)
        
                voxelarray[I] = True
                voxelcolors[I] = colors[ind%len(colors)]
        
        ax.voxels(voxelarray, edgecolor='k',facecolors=voxelcolors)
        return ax, voxelarray

    def vol(self):
        
        vol = 0
        
        for cube in self.cubes:
            
            vol += cube.vol()
            
        return vol
    
    def __repr__(self):
        
        return ''.join([str(cube)+'\n' for cube in self.cubes])
        

class QuantumDiceGameUniverses():
    
    def __init__(self, start1, start2, score_threshold, nfaces=3, nthrows=3):
        
        root_name = f'{start1},{start2};'
       
        
        self.score_threshold = score_threshold
        
        self.info_dict = {}
        self.nfaces = nfaces
        self.nthrows = nthrows
        
        self.path_levels = [set([root_name])] + [set([]) for i in range(score_threshold)] # allocate ample space for levels
        self.info_dict[root_name] = (0,0,1)  #score1, score2, weight of path
        
        self.wins = [0,0]
        
        self.terminal_nodes = set([])


    def add_node(self, node_name, weight, level,  parent_name):
        
        t0 = timer()
        parent_score0, parent_score1, parent_weight = self.info_dict[parent_name]
        score1,score2 = self.score(node_name, parent_score0,parent_score1)
        node_weight = weight*parent_weight
        
        t1 = timer()
        
        if score1 >= self.score_threshold:   
            self.wins[0] += node_weight
        elif score2 >= self.score_threshold: 
            self.wins[1] += node_weight
        else:
            self.path_levels[level].add(node_name)
            self.info_dict[node_name] = (score1,score2,node_weight)
            
        t2 = timer()

        return t2-t1,t1-t0
        
        
    def score(self, node_name, parent_score0, parent_score1):
                   
        node_name_split = node_name.split(';')[0].split(',')
       
        score0 = parent_score0 + int(node_name_split[0])
        score1 = parent_score1 + int(node_name_split[1])

        return (score0,score1)
    
        
    def return_wins(self):
        
        return int(self.wins[0]/(self.nfaces**self.nthrows)),int(self.wins[1])  # the division accounts for the fact that 
                                                                      # if first player wins, the game ends    
                                                                      # and player 2 does not get to play the next turn
                                                                      # which acounts for a factor of nfaces**nthrows universes
    

class SnailNumberTree():
    
    def __init__(self, string=None, tree=None):
        
        
        '''
        This is a binary operation tree for day 18 of advent of code 2021
        Operations are defined in the respective page. If given an operation 
        string it initializes the tree associated to it otherwise it can be 
        initialized directly by an operation tree.
        
        An operation like [5,3] would lhave three nodes a root node ,
        then two children 5 and 3. It generalizes similarly to 
        higher operations.
    
        
        '''
        
        
        if tree is not None:
            self.tree = tree
        elif string is not None:
            self.tree = str_to_tree(string)
        else:
            self.tree = None
        
        self.levels = []
        
        if self.tree is not None:
            self.add_nodes(self.tree)
        
    def add_nodes(self, tree):
        
        for node in tree.descendants:
            if self.is_numeric(node):
                depth = str(node).count(',')-1
                
                if len(self.levels)<depth+1:
                    self.levels += [[] for i in range(depth+1 - len(self.levels))]
                
                self.levels[depth].append(node)
        
    def copy(self):
        
        tree = SnailNumberTree()
        tree.tree = self.tree
        
        tree.levels = self.levels
        
        
        return tree
        
        
    def join_to(self,tree):
        
        joined_tree = SnailNumberTree(tree=Node(',',children=[copy_anytree(self.tree),copy_anytree(tree.tree)]))
        joined_tree.reduce()
        
        return joined_tree

    def depth(self):
        
        return sum([1 for x in self.levels if any(y.isnumeric() for y in str(x))])

    def is_numeric(self, node):
        
        return any(x.isnumeric() for x in str(node))


    def reduce(self):
        
        if len(self.levels)>=5:
            self.explode()
        
        
        node = self.find_first_reduce_node()

        
        while node is not None:
                                    
            num1 = int(np.floor(int(node.name)/2))
            num2 = int(np.ceil(int(node.name)/2))
            
            node.name = ','
            
            Node(str(num1),parent=node)
            Node(str(num2),parent=node)
            
            self = SnailNumberTree(tree=self.tree)
            
            if len(self.levels)>=5:
                self.explode()
            
            node = self.find_first_reduce_node()
            
                
    def explode(self):
        
        depth = len(self.levels)
        
        while depth>=5:
            
            level = self.levels[-1]
            nodes = [node for node in level if self.is_numeric(node)]
            
            while len(nodes)>0:
                
                node1 = nodes[0]
                node2 = nodes[1]
                parent = node1.parent
                
                grandparent = parent.parent
                rind = grandparent.children.index(parent)
                
                lnode = self.find_first_left(len(self.levels)-1,0)
                rnode = self.find_first_right(len(self.levels)-1,1)
                
                if lnode is not None:
                    lnode.name = str(int(lnode.name) + int(node1.name))
                if rnode is not None:
                    rnode.name = str(int(rnode.name) + int(node2.name))
                
                parent.parent = None
                Node(0,parent=grandparent)
                
                if rind == 0:
                    grandparent.children = [grandparent.children[x] for x in [1,0]]
                    
                self = SnailNumberTree(tree=self.tree)
                
                nodes = nodes[2:]

            depth = len(self.levels)          
                        

    def find_first_left(self, depth,index):
        
        level = self.levels[depth]
        
        node = level[index]
        
        parent = node.parent
        
        while parent is not None and parent.children.index(node)==0:
            node = parent
            parent = node.parent
            
        if parent is None:
            return None
        else:
            node = parent.children[0]
            
            while len(node.children)>0:
                node = node.children[1]
                
            return node
       
    def find_first_right(self, depth,index):
      
        level = self.levels[depth]
        
        node = level[index]
        
        parent = node.parent
        
        while parent is not None and parent.children.index(node)==1:
            node = parent
            parent = node.parent
            
        if parent is None:
            return None
        else:
            node = parent.children[1]
            
            while len(node.children)>0:
                node = node.children[0]
                
            return node

    def find_first_reduce_node(self):
        
        for node in self.tree.descendants:

            if self.is_numeric(node) and int(node.name)>=10:
                return node
            
        return None
            
    def numeric_nodes(self):
        
        return [node for node in self.tree.descendants if self.is_numeric(node)]

    def sum(self):
        
        return sum_tree(self.tree)

    
    def print_levels(self):
        
        for level in self.levels:
            print(level)


    def ascii_render(self):   
        
        return str(RenderTree(self.tree))


    def __str__(self):
        
        return tree_to_str(self.tree)
        
def copy_anytree(node):
    
    if len(node.children)==0:
        return Node(node.name)
    
    else:
        return Node(node.name, children = [copy_anytree(child) for child in node.children])
        
    

def sum_tree(root):
    
    if len(root.children) == 0:
        
        return int(root.name)
    
    else:
        
        lchild = root.children[0]
        rchild = root.children[1]
        
        return 3*sum_tree(lchild) + 2*sum_tree(rchild)
 
   
def tree_to_str(root):
        
        
    if len(root.children)==0:
        return root.name
    
    else:
        
        lpart = tree_to_str(root.children[0])
        rpart = tree_to_str(root.children[1])
        
        return f'[{lpart},{rpart}]'
        
        
def str_to_tree(string, depth=0):
    
    queue = []
    
    assert all(x.isnumeric() or x in [',','[',']'] for x in string), f'String {string} is invalid'
    
    try:
        [queue.append('1') if x=='[' else queue.pop(len(queue)-1) if x==']' else 'idle' for x in string]
    except IndexError:
        raise ValueError(f'String {string} is invalid')
            
    if len(queue)>0:
        raise ValueError(f'String {string} is invalid')
    
    left,right = split(string)
            
    if left.isnumeric():
        left_tree = Node(left)
    else:
        left_tree = str_to_tree(left,depth+1)
        
    if right.isnumeric():
        right_tree = Node(right)
    elif right != '':
        right_tree = str_to_tree(right,depth+1)
    else:
        right_tree = None
   
    if right_tree is None:
        joined_tree =  left_tree
    
    else:
        joined_tree = Node(',', children=[left_tree, right_tree])
     
    return joined_tree 
    
    
def split(string):
    
    if '[' not in string:
        return string,''
    
    else:
        queue = []

        for ind,x in enumerate(string):
            
            if x=='[':
                queue.append('[')
            elif x==']':
                queue.pop(len(queue)-1)
        
            elif x==',' and len(queue)==1:
                
                return string[1:ind],string[ind+1:-1]
    

    
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
    dijkstra_algorithm is from udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html
    others: Sina Tureli
    '''
    def __init__(self):
        
        self._nodes = []
        self._node_map = {}
        self._number_of_nodes = 0
        self.adjacency_set = {}
        self.weights = {}
        self.max_visits = {}

    def get_nodes(self):
        return list(self._node_map.keys())
            
    def add_node(self,node_name, max_visits=1):

        if node_name not in self._node_map:
            self._nodes.append(node_name)
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
            self.weights[(node_name2,node_name1)] = 1
        if node_name2 not in self.adjacency_set[node_name1]:
            self.adjacency_set[node_name1].append(node_name2)
            self.weights[(node_name1,node_name2)] = 1

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

    def path_len(self, path):
        
        return sum([self.weights[(path[i],path[i+1])] for i in range(len(path)-1)])

    def djikstras_algorithm(self,start):
        
        previous_nodes = {}
        
        unvisited_nodes = [x for x in self._nodes]
        distances = {node : np.inf for node in self._nodes if node!=start}
        distances[start]=0

        while len(unvisited_nodes)>0:
            current_min_node = None
            
            for node in unvisited_nodes: # Iterate over the nodes
            
                if current_min_node == None:
                    current_min_node = node
                elif distances[node] < distances[current_min_node]:
                    current_min_node = node
                    
                    
            neighbors = self.adjacency_set[current_min_node]
            
            for neighbor in neighbors:
                tentative_value = distances[current_min_node] + self.weights[(current_min_node, neighbor)]
                if tentative_value < distances[neighbor]:
                    distances[neighbor] = tentative_value
                    # We also update the best path to the current node
                    previous_nodes[neighbor] = current_min_node
                    
            unvisited_nodes.remove(current_min_node)
            
            
            
        return previous_nodes,distances

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
            
            if end in graph[start]:
                path.append(end)
                
                return path
            
            for node in graph[start]:
                if node not in path:
                    newpath = self.find_shortest_path(start=node, end=end, path=path)
                    if newpath:
                        if not shortest or self.path_len(newpath) < self.path_len(shortest):
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

def dijkstra(G, s):
    
    '''
    Author of this algorithm is Enzo Lizama from stackoverflow
    https://stackoverflow.com/questions/22897209/dijkstras-algorithm-in-python
    '''
    
    n = len(G)
    visited = [False]*n
    weights = [math.inf]*n
    path = [None]*n
    queue = []
    weights[s] = 0
    hq.heappush(queue, (0, s))
    while len(queue) > 0:
        g, u = hq.heappop(queue)
        visited[u] = True
        for v, w in G[u]:
            if not visited[v]:
                f = g + w
                if f < weights[v]:
                    weights[v] = f
                    path[v] = u
                    hq.heappush(queue, (f, v))
    return path, weights

def flatten_iterable(input_iter):
    
    flat_iterable = []
    
    for elem in input_iter:
        if hasattr(elem,'__iter__'):
            flat_iterable += flatten_iterable(elem)
        else:
            flat_iterable.append(elem)
            
    return flat_iterable
        
        

def split_list(lst, value):
    indices = [i for i, x in enumerate(lst) if x == value]
    split_list = []
    
    for i0,i1 in zip([-1, *indices], [*indices, len(lst)]):
        split_list.append(lst[i0+1:i1])
        
    return split_list

        

def binary_to_decimal(vec):
    
    vec = list(vec)
    
    return sum([vec[::-1][i]*2**i for i in range(len(vec))])


def intersect_intervals(x,y):
    
    if x[1]<y[0] or x[0]>y[1]:
        return []
    else:
        return [max(min(x[0],y[1]),y[0]),min(max(x[1],y[0]),y[1])]


