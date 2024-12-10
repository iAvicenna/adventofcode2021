#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from adventofcode2021.utils import Graph

def is_node_final(node):
    
    node_split = node.split('_')
    
    A = [int(x) for x in node_split[0:4]]
    B = [int(x) for x in node_split[4:8]]
    C = [int(x) for x in node_split[8:12]]
    D = [int(x) for x in node_split[12:16]]
    
    return set(A) == set(range(11,15)) and set(B) == set(range(15,19)) and set(C) == set(range(19,23)) and set(D) == set(range(23,27))
    

def is_move_admissible(current_state, next_state, amph_index):
    
    amph_rooms = room_indices[amph_index]
    amph_forbidden_rooms = forbidden_room_indices[amph_index]
    others = [ind for ind in range(N_amp) if int(ind/4)!=int(amph_index/4)]
    
    current_pos = current_state[amph_index]
    next_pos = next_state[amph_index]
    
    others_in_amph_rooms = any(next_state[x] in amph_rooms for x in others)
    
    if next_state.count(next_pos)>1:
        return False
    
    if next_pos in junction_indices:
        return False
    
    if current_pos not in amph_forbidden_rooms and next_pos in amph_forbidden_rooms:
        return False
    
    if current_pos in hallway_indices and next_pos not in amph_rooms:
        return False
    
    if next_pos in amph_rooms and others_in_amph_rooms:
        return False
    
    return True


def player_adjacency_sets(state, index, adjacency_sets):
    
    
    cut = []
    new_adjacency_sets = adjacency_sets.copy()
    
    for ipos,pos in enumerate(state):
        if index != ipos:
            cut.append(pos)
                   
    for ind in range(len(adjacency_sets)):
        
        if ind not in cut:
            new_adjacency_sets[ind] = [x for x in new_adjacency_sets[ind] if x not in cut]
        
        else:
            new_adjacency_sets[ind] = []
            
    return new_adjacency_sets
    

def read_input(file_path):
    
    input_lines = list(map(str.rstrip,open(file_path,'r')))
    
    amp_indices = [[],[],[],[]]
    amp_types = ['A','B','C','D']
    if len(input_lines)==7:
        
        indices = [[11,15,19,23],
                   [12,16,20,24],
                   [13,17,21,25],
                   [14,18,22,26]
                   ]
        
        
        for iline,line in enumerate(input_lines[2:6]):
            
            amps = [x for x in line if x in ['A','B','C','D']]
        
            I = [amp_types.index(x) for x in amps]
            [amp_indices[i].append(indices[iline][indi]) for indi,i in enumerate(I)]               

    return [x for z in amp_indices for x in sorted(z)]


initial_state = read_input('input2.txt')


#initial_state = read_input('test_input2.txt')
#initial_state = read_input('input2.txt')
N_amp = len(initial_state)

N=27
base_adjacency_sets = [
    [1],        # 0
    [0,2],      # 1
    [1,3,11],   # 2
    [2,4],      # 3
    [3,5,15],   # 4
    [4,6],      # 5
    [5,7,19],   # 6
    [6,8],      # 7
    [7,9,23],   # 8
    [8,10],     # 9
    [9],        # 10
    [2,12],     # 11
    [11,13],    # 12
    [12,14],    # 13
    [13],       # 14
    [4,16],     # 15
    [15,17],    # 16
    [16,18],    # 17
    [17],       # 18
    [6,20],     # 19
    [19,21],    # 20
    [20,22],    # 21
    [21],       # 22
    [8,24],     # 23
    [23,25],    # 24
    [24,26],    # 25
    [25],       # 26
    
    ]  

base_graph = Graph()
[base_graph.add_node(i) for i in range(N)]
[base_graph.connect_nodes(i,j) for i in range(N) for j in base_adjacency_sets[i]]
distances = np.zeros((N,N))

for i in range(N):
                
    _,dists = base_graph.djikstras_algorithm(i)
        
    for j in range(N):
        distances[i,j] = dists[j]
    
cost = [1,1,1,1,10,10,10,10,100,100,100,100,1000,1000,1000,1000]
    
junction_indices = set([2,4,6,8])
hallway_indices = list(range(11))
room_indices = [[11,12,13,14] for _ in range(4)] + [[15,16,17,18] for _ in range(4) ] + [[19,20,21,22] for _ in range(4)] + [[23,24,25,26] for _ in range(4)]

forbidden_room_indices = [list(range(15,27)) for _ in range(4)] + [[11,12,13,14]+list(range(19,27)) for _ in range(4)] + [list(range(11,19)) + [23,24,25,26] for _ in range(4)] + [list(range(11,23))  for _ in range(4)]

pair_indices = [[1,2,3],[0,2,3],[0,1,3],[0,1,2],
                [5,6,7],[4,6,7],[4,5,7],[4,5,6],
                [9,10,11],[8,10,11],[8,9,11],[8,9,10],
                [13,14,15],[12,14,15],[12,13,15],[12,13,14]]


base_room_graph = Graph()
[base_room_graph.add_node(i) for i in range(N)]
[base_room_graph.connect_nodes(i0, i1) for i0 in range(N) for i1 in base_adjacency_sets[i0]]
current_states = [initial_state.copy()]

game_nodes = set([])
game_nodes.add('_'.join([str(x) for x in current_states[0]]))

counter = -1
node_distances = {'_'.join([str(x) for x in current_states[0]]):0}
distance_threshold = np.inf

while len(current_states)>0:
    
    counter += 1
    new_states = []
    print(counter)

    
    for current_state in current_states:

        current_node = '_'.join([str(x) for x in current_state])
        
        for ind0 in range(N_amp):
            pair_index_set = pair_indices[ind0]
            
            if ((current_state[ind0] in room_indices[ind0] and all(current_state[pi] in room_indices[ind0] for pi in pair_index_set))
                or current_state[ind0] == room_indices[ind0][3] 
                or (current_state[ind0] == room_indices[ind0][2] and any(current_state[pi] == room_indices[ind0][3] for pi in pair_index_set))
                or (current_state[ind0] == room_indices[ind0][1] and any(current_state[pi] == room_indices[ind0][2] for pi in pair_index_set) and any(current_state[pi] == room_indices[ind0][3] for pi in pair_index_set))
                ):
                
                pass
            
            else:
                new_adj_sets = player_adjacency_sets(current_state, ind0, base_adjacency_sets)
                base_room_graph.adjacency_set = {ind1:[] for ind1 in base_room_graph.adjacency_set}
                [base_room_graph.connect_nodes(i0, i1) for i0 in range(N) for i1 in new_adj_sets[i0]]
                
                player_new_states = base_room_graph.connected_component(current_state[ind0])
                
                to_remove = set(current_state).union(junction_indices).union(
                    [z for ind1,r in enumerate(room_indices) for z in r if int(ind0/4) != int(ind1/4)])
                
                player_new_states = player_new_states.difference(to_remove)
                
                for player_state in player_new_states:
                    
                    
                    distance = distances[current_state[ind0],player_state]*cost[ind0]
                    new_state = current_state.copy()
                    new_state[ind0] = player_state
                    
                  
                    if is_move_admissible(current_state,new_state,ind0) and distance<=distance_threshold:
    
                        new_node = '_'.join([str(x) for x in new_state])
                        new_node_distance = node_distances[current_node] + distance
                        
                        if new_node not in node_distances:
                            node_distances[new_node] = new_node_distance
                        else:
                            node_distances[new_node] = min(node_distances[new_node],new_node_distance)
                            
                        if is_node_final(new_node):
                            distance_threshold = min([distance_threshold,node_distances[new_node]])
                            print(distance_threshold)
                        
                        if new_node not in game_nodes:
                            game_nodes.add(new_node)
                            new_states.append(new_state)
                            
    current_states = new_states.copy()
    
for node in game_nodes:
        
    if is_node_final(node):
        
        print(f'{node} {int(node_distances[node])}')        
        
for node in game_nodes:
    
    split_node = [int(x) for x in node.split('_')]
    
    if (set(split_node[0:4]) == set([11,12,13,14]) 
        ):
        
        print(node)
    
    