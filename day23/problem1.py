#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import itertools as it
import numpy as np
from adventofcode2021.utils import Graph

def is_move_admissible(current_state, next_state, amph_index):
    
    amph_rooms = room_indices[amph_index]
    amph_forbidden_rooms = forbidden_room_indices[amph_index]
    others = [ind for ind in range(8) if int(ind/2)!=int(amph_index/2)]
    
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
    



#0,1,2,3,4,5,6,7
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
initial_state = [12,18,11,15,13,16,14,17]
#initial_state = [18,12,15,11,16,13,17,14]

  
#############
#...........#
###D#A#A#D###
  #C#C#B#B#
  #########  
#initial_state = [13,15,16,18,12,14,11,17]
N = 11+2*4


# 0  1  2  3  4  5  6  7  8  9  10
#      11    13    15    17
#      12    14    16    18

base_adjacency_sets = [
    [1],        # 0
    [0,2],      # 1
    [1,3,11],   # 2
    [2,4],      # 3
    [3,5,13],   # 4
    [4,6],      # 5
    [5,7,15],   # 6
    [6,8],      # 7
    [7,9,17],   # 8
    [8,10],     # 9
    [9],        # 10
    [2,12],     # 11
    [11],       # 12
    [4,14],     # 13
    [13],       # 14
    [6,16],     # 15
    [15],       # 16
    [8,18],     # 17
    [17],       # 18
    ]  

base_graph = Graph()
[base_graph.add_node(i) for i in range(N)]
[base_graph.connect_nodes(i,j) for i in range(N) for j in base_adjacency_sets[i]]
distances = np.zeros((N,N))

for i in range(N):
                
    _,dists = base_graph.djikstras_algorithm(i)
        
    for j in range(N):
        distances[i,j] = dists[j]
    
cost = [1,1,10,10,100,100,1000,1000]
    
junction_indices = set([2,4,6,8])
hallway_indices = list(range(11))
room_indices = [[11,12],[11,12],[13,14],[13,14],[15,16],[15,16],[17,18],[17,18]]
forbidden_room_indices = [list(range(13,19)),list(range(13,19)),
                   [11,12,15,16,17,18],[11,12,15,16,17,18],
                   [11,12,13,14,17,18],[11,12,13,14,17,18],
                   list(range(11,17)),list(range(11,17))]
pair_indices = [1,0,3,2,5,4,7,6]




final_nodes = it.product(['11_12','12_11'],['13_14','14_13'],['15_16','16_15'],['17_18','18_17'])
final_nodes = ['_'.join([str(y) for y in x]) for x in final_nodes]

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

    print(counter)
    counter += 1
    new_states = []
    
    for current_state in current_states:

        
        current_node = '_'.join([str(x) for x in current_state])
        
        for ind0 in range(8):
            pair_index = pair_indices[ind0]
            
            if ((current_state[ind0] in room_indices[ind0] and current_state[pair_index] in room_indices[ind0]) 
                or current_state[ind0] == room_indices[ind0][1]):
                
                pass
            
            else:
                new_adj_sets = player_adjacency_sets(current_state, ind0, base_adjacency_sets)
                base_room_graph.adjacency_set = {ind1:[] for ind1 in base_room_graph.adjacency_set}
                [base_room_graph.connect_nodes(i0, i1) for i0 in range(N) for i1 in new_adj_sets[i0]]
                
                player_new_states = base_room_graph.connected_component(current_state[ind0])
                
                to_remove = set(current_state).union(junction_indices).union(
                    [z for ind1,r in enumerate(room_indices) for z in r if int(ind0/2) != int(ind1/2)])
                
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
                            
                        if new_node in final_nodes:
                            distance_threshold = min([distance_threshold,node_distances[new_node]])
                        
                        if new_node not in game_nodes:
                            game_nodes.add(new_node)
                            new_states.append(new_state)
                            
    current_states = new_states.copy()
    
final_nodes = []
for node in game_nodes:
    
    node_split = node.split('_')
    
    if ('_'.join(node_split[0:2]) in ['11_12','12_11'] and
        '_'.join(node_split[2:4]) in ['13_14','14_13'] and 
        '_'.join(node_split[4:6]) in ['15_16','16_15'] and
        '_'.join(node_split[6:8]) in ['17_18','18_17']
        ):
        print(f'{node} {node_distances[node]}')        
        
    
    
    