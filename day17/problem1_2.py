#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def find_admissible_n_from_vx(vx,xrange):
    
    '''
    Given a speed vx in x direction, we can compute
    its x position after n iterations. By requiring this
    to be in the given xrange, we can find the range
    of admissible n's that are allowed. It only looks until
    vx + 1, if vx + 1 is admissible since vx = 0 at this point
    then any n after this is also allowed and this is handled seperately.
    '''
    
    admissible_n = []
    
    x0 = xrange[0]
    x1 = xrange[1]
    
    for n in range(1,vx+1):
        
        pos = n*vx - n*(n-1)/2
        
        if pos<=x1 and pos>=x0:
            admissible_n.append(n)
            
            
    return admissible_n

def solve_problem1_2(input_path):
    
    with open(input_path,'r') as fp: 
        data = list(map(str.rstrip,fp))[0].split(': ')[-1].split(', ')
    
    
    xrange = list(map(int,data[0].split('=')[-1].split('..')))
    yrange = list(map(int,data[1].split('=')[-1].split('..')))
    
    admissible_pairs = []
    admissible_x = []
    admissible_y = []
    
    # the x range puts an upper and lower bound on vx. 
    # so we have a range of admissible vx. Each vx value also has a list
    # of admissible n's, otherwise the probe would fly out of the required
    # range so now we have a given vx, and a list of admissible ns. 
    # given n and a y position, we can find the vy required to fall in this position 
    # 
    # Note that if for a given vx, if n=vx is admissible, than any n after this is 
    # admissible in theory. However looking after a certain value of n is of no use
    # due to restriction on vy which requires vy + 1 < max(abs(yrange)).
    
    for vx in range(1,xrange[1]+1):
        admissible_n = find_admissible_n_from_vx(vx,xrange)
        
        if len(admissible_n)>0 and admissible_n[-1]==vx:
            admissible_n += list(range(vx,vx+3*max(abs(yrange[0]),yrange[1])))
        
        for n in admissible_n:
            
            for vy in range(yrange[0]-1,78):
                ypos = n*vy - n*(n-1)/2
                
                if ypos>=yrange[0] and ypos<=yrange[1]:
                    if (vx,vy) not in admissible_pairs:
                        admissible_pairs.append((vx,vy))
                        admissible_x.append(vx)
                        admissible_y.append(vy)
        
        
    return admissible_y
          

if __name__ == '__main__':
    
    admissible_y = solve_problem1_2('test_input1.txt')
    
    max_y = max(admissible_y)
    max_height = max_y*max_y/2 + max_y/2
    
    print('Problem 1 Test')
    print(int(max_height))
    print('Problem 2 Test')
    print(len(admissible_y))
    assert int(max_height) == 45
    assert len(admissible_y) == 112
    
    admissible_y = solve_problem1_2('input1.txt')
    
    max_y = max(admissible_y)
    max_height = max_y*max_y/2 + max_y/2
    
    print('')
    
    print('Problem 1')
    print(int(max_height))
    print('Problem 2')
    print(len(admissible_y))
    
    assert int(max_height) == 3003
    assert len(admissible_y) == 940
    
    
    
    
    
    