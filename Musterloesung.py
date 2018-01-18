# -*- coding: utf-8 -*-
"""
Created on Tue Jan 09 00:10:53 2017

@author: Johannes Schrumpf und Anton Laukemper
"""

import numpy as np
import random

class mdp:
    def __init__(self, grid, exit_value, pitfall_value, reward_value, discount_value):
        self.structure_mat = grid
        self.discount = discount_value
        self.exit_value = exit_value
        self.pitfall_value = pitfall_value
        self.reward_value = reward_value
        self.value_matrix = self.initalize_values(self.structure_mat)
        print("initial value matrix:")
        print(self.value_matrix)
        self.policy = self.initalize_policy(self.structure_mat)
        print("initial policy matrix:")
        print(self.policy)

        self.policy_evaluation_helper(0, 2, "d")
# - - - - - - - - - - - - - - I N I T I A L I Z E  M D P - - - - - - - - - - - - - - - - - - - - 
         
    def load_and_parse(self, file):
        parsed_mat = np.loadtxt(file + ".grid", dtype = str)
        return parsed_mat
    
    def initalize_values(self, structure):
        
        shape = structure.shape
        newmat = np.empty(shape)
        
        xdim = shape[1]
        ydim = shape[0]
        
        for yindex in range(ydim):
            for xindex in range(xdim):
                if structure[yindex][xindex] == "F":
                    newmat[yindex][xindex] = self.reward_value
                elif structure[yindex][xindex] == "E":
                    newmat[yindex][xindex] = self.exit_value
                elif structure[yindex][xindex] == "P":
                    newmat[yindex][xindex] = self.pitfall_value
                elif structure[yindex][xindex] == "O":
                    newmat[yindex][xindex] = None
        return newmat
        
    def initalize_policy(self, structure):
        shape = structure.shape
        newmat = np.empty(shape, dtype = str)
        
        policy_array = ["up","down","right","left"]
        
        xdim = shape[1]
        ydim = shape[0]
        
        for yindex in range(ydim):
            for xindex in range(xdim):
                if structure[yindex][xindex] == "F":
                    newmat[yindex][xindex] = random.choice(policy_array)
                elif structure[yindex][xindex] == "E" or structure[yindex][xindex] == "P":
                    newmat[yindex][xindex] = "stay"
                else:
                    newmat[yindex][xindex] = "N"
        return newmat
    
        
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - U P D A T E  V A L U E S  &  P O L I C Y - - - - - - - - - - - - - - - - - - - -        
    def state_transition_prob(self, x, y, _x, _y, action):
        grid = self.structure_mat
        #returns the probability to land in grid[_x][_y], given you are in grid[x][y] and do action "action"
        delta_x = _x-x
        delta_y = _y-y
        #if you want to move diagonally or more than one cell, return 0, since that's not possible
        if((delta_x)**2>1 or (delta_y)**2>1 or ((delta_x)**2==1 and (delta_y)**2==1) ):
            return 0
        try:
            #if destination is an obstacle...
            if(grid[_x][_y]=="O"):
                return 0
        except IndexError:
            #...or if it is outside of the maze, return 0
            return 0
            
        
        if(delta_x>0):
            #We want to move down
            if(action=="d"):
                return 0.8
            if(action=="l" or action=="r"):
                return 0.1
            
        if(delta_x<0):
            #We want to move up
            if(action=="u"):
                return 0.8
            if(action=="l" or action=="r"):
                return 0.1
            
        if(delta_y>0):
            #We want to move right
            if(action=="r"):
                return 0.8
            if(action=="u" or action=="d"):
                return 0.1
            
        if(delta_y<0):
            #We want to move left
            if(action=="l"):
                return 0.8
            if(action=="u" or action=="d"):
                return 0.1
            
        #case that we want to find the probability to stay in original state:
        #here we need to check whether the neighbouring cells, where we could end up if doing action 
        #"action" are actually obstacles. If that is the case, it increases the probability that we stay where we are
        if(delta_x==0 and delta_y==0):
            prob = 0
            if(action=="r"):
                #we technically want to go right
                try:
                    #but if there is an obstacle...
                    if(grid[x][y+1]=="O"):
                        #we probably stay where we are
                        prob += 0.8
                except IndexError:
                    #same happens, if we would move outside of the field
                    prob += 0.8

                try:
                    if(grid[x+1][y]=="O"):
                        prob += 0.1
                except IndexError:
                    prob += 0.1
                try:
                    if(grid[x-1][y]=="O"):
                        prob += 0.1
                    
                    if(x-1<0): #it's not an index error in python if you call an array with negative values, so I do this manually lol
                        raise IndexError
                except IndexError:
                    prob += 0.1

                return prob

            if(action=="d"):
                try:
                    if(grid[x+1][y]=="O"):
                        prob += 0.8
                except IndexError:
                    prob += 0.8

                try:
                    if(grid[x][y+1]=="O"):
                        prob += 0.1
                except IndexError:
                    prob += 0.1
                try:
                    if(grid[x][y-1]=="O"):
                        prob += 0.1
                    if(y-1<0):
                        raise IndexError
                except IndexError:
                    prob += 0.1

                return prob

            if(action=="l"):
                try:
                    if(grid[x][y-1]=="O"):
                        prob += 0.8
                    if(y-1<0):
                        raise IndexError
                except IndexError:
                    prob += 0.8

                try:
                    if(grid[x+1][y]=="O"):
                        prob += 0.1
                except IndexError:
                    prob += 0.1
                try:
                    if(grid[x-1][y]=="O"):
                        prob += 0.1
                    if(x-1<0):
                        raise IndexError
                except IndexError:
                    prob += 0.1

                return prob

            if(action=="u"):
                try:
                    if(grid[x-1][y]=="O"):
                        prob += 0.8
                    if(x-1<0):
                        raise IndexError
                except IndexError:
                    prob += 0.8

                try:
                    if(grid[x][y+1]=="O"):
                        prob += 0.1
                except IndexError:
                    prob += 0.1
                try:
                    if(grid[x][y-1]=="O"):
                        prob += 0.1
                    if(y-1<0):
                        raise IndexError
                except IndexError:
                    prob += 0.1

                return prob    
        return 0
     
     
     
        # gives the reward for doing action "action" in the cell [x,y]
    def reward(self, x, y, action):
        grid = self.structure_mat
        if(grid[x][y]=="F"):
            #existance is pain... just moving gives us the "reward" of the penalty that the user has set
            return self.reward_value
        if(grid[x][y]=="E"):
            return self.exit_value
        if(grid[x][y]=="P"):
            return self.pitfall_value
        return 0
    
        # one step of the policy evaluation
    def policy_evaluation(self):
        grid = self.structure_mat
        values = np.zeros(grid.shape)
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if(grid[i][j] == "O"): # value of cells with obstacles should remain None
                    values[i][j] = None 
                elif(grid[i][j] == "E"): # value of the cell with the exit, should not change
                    values[i][j] = self.exit_value
                elif(grid[i][j] == "P"): # same with pitfall
                    values[i][j] = self.pitfall_value
                else:
                    #see slide 40 for algorithm
                    # the new value for a cell is the current reward in the cell (so mostly the movement penalty)
                    # plus the probality to end up in a neighbouring cell * the reward of that cell
                    # for each cell that we could end up in, given our current policy matrix
                    # if(i==0 and j==2):
                    #     print("hello")
                    #     print(self.policy[i][j])
                    #     print(self.policy_evaluation_helper(i, j, self.policy[i][j]))
                    #     print("bye")
                    # print(self.reward(i,j, self.policy[i][j]) + self.discount * self.policy_evaluation_helper(i, j, self.policy[i][j]))
                    values[i][j]= self.reward(i,j, self.policy[i][j]) + self.discount * self.policy_evaluation_helper(i, j, self.policy[i][j])
        self.value_matrix = values

    #this is just a part of the algorithm on slide 40
    def policy_evaluation_helper(self, x,y, action):
        grid = self.structure_mat
        summe = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if(np.isnan(self.value_matrix[i][j])):
                    summe = summe  # add nothing
                else:
                    summe += self.state_transition_prob(x, y, i, j, action) * self.value_matrix[i][j]
        print(summe)
        return summe


    def update_values(self):
        
        discount = self.discount
        struct = np.copy(self.structure_mat)
        values = np.copy(self.value_matrix)
        policy = np.copy(self.policy)
        new_values = np.copy(values)
        bounds = values.shape
        
        for yindex in range(bounds[0]):
            for xindex in range(bounds[1]):
                current_value = values[yindex][xindex]
                
                if yindex == 0 or struct[yindex - 1][xindex] == "O":
                    up = current_value
                else:
                    up = values[yindex - 1][xindex]
                
                if yindex == bounds[0] - 1 or struct[yindex + 1][xindex] == "O":
                    down = current_value
                else:
                    down = values[yindex + 1][xindex]
                
                if xindex == 0 or struct[yindex][xindex - 1] == "O":
                    left = current_value
                else:
                    left = values[yindex][xindex - 1]
                
                if xindex == bounds[1] - 1 or struct[yindex][xindex + 1] == "O":
                    right = current_value
                else:
                    right = values[yindex][xindex + 1]
                
                if policy[yindex][xindex] == "u":
                    new_value = discount * (up * 0.8 + left * 0.1 + right * 0.1) -0.04
                elif policy[yindex][xindex] == "d":
                    new_value = discount * (down * 0.8 + left * 0.1 + right * 0.1) -0.04
                elif policy[yindex][xindex] == "l":
                    new_value = discount * (left * 0.8 + up * 0.1 + down * 0.1) - 0.04
                elif policy[yindex][xindex] == "r":
                    new_value = discount * (right * 0.8 + up * 0.1 + down * 0.1) -0.04
                else:
                    new_value = current_value
                new_values[yindex][xindex] = new_value
        self.value_matrix = new_values
        return
    


     # here we want to change the policy
    # see slide 49 for algorithm
    def policy_update(self):
        policy_matrix = self.policy
        value_matrix = self.value_matrix
        _policies = policy_matrix
        for i in range(len(policy_matrix)):
            for j in range(len(policy_matrix)):
                    # for each cell we want to check which action would give us the best result
                    maximum = 0
                    policy = "r"
                    for action in ["u","d","r","l"]:
                        new = self.reward(i,j, action) + self.discount * self.policy_evaluation_helper(i,j, action)
                        #print(new)
                        if (new > maximum): 
                            maximum = new
                            policy = action
                    _policies[i][j] = policy
        self.policy = _policies
        return 


    def update_policy(self):
        struct = np.copy(self.structure_mat)
        values = np.copy(self.value_matrix)
        new_policy = np.copy(self.policy)
        bounds = values.shape
        for yindex in range(bounds[0]):
            for xindex in range(bounds[1]):
                
                if (
                        struct[yindex][xindex] == "O" or
                        struct[yindex][xindex] == "E" or
                        struct[yindex][xindex] == "P"
                    ):
                    continue
                celllist = []
                if yindex == 0:
                    celllist.append(["u",-100])
                else:
                    celllist.append(["u",values[yindex - 1][xindex]])
                    
                if yindex == bounds[0] - 1:
                    celllist.append(["d", -100])
                else:
                    celllist.append(["d",values[yindex - 1][xindex]])
                    
                if xindex == 0:
                    celllist.append(["l", -100])
                else:
                    celllist.append(["l", values[yindex][xindex - 1]])
                    
                if xindex == bounds[1] - 1:
                    celllist.append(["r", -100])
                else:
                    celllist.append(["r",values[yindex][xindex + 1]])
                
                choice = ["s", -500]
                for element in celllist:
                    if element[1] > choice[1]:
                        choice = element
                cellmove = choice[0]
                
                new_policy[yindex][xindex] = cellmove
        self.policy = new_policy
        return
                
                
                
        
        
                        
            
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - U I - - - - - - - - - - - - - - - - - - - - - -   
def initalize():
   
    # I would suggest we only give the 3 options for the grids. They need to be in the same folder
    grid1 = np.genfromtxt("3by4.grid", dtype='str')
    grid2 = np.genfromtxt("5by10.grid", dtype='str')
    grid3 = np.genfromtxt("9by17.grid", dtype='str')

    grid_choice = 5

    while (grid_choice >3 or grid_choice < 1):
        try:
            grid_choice = int(raw_input("Please choose from one of the three gridworlds: \n (1) 3by4 matrix \n (2) 5by10 matrix \n (3) 9by17 matrix \n Please indicate your choice by typing 1, 2 or 3: "))
        except ValueError:
            print("Oh noes! you typed in a wrong number!!! please try a number between 1 and 3: ")
        #storing the grid that the user selected
    if (grid_choice == 1):
        grid = grid1
    elif (grid_choice == 2):
        grid = grid2
    else:
        grid = grid3
    print("you chose \n"+ str(grid) )
    #setting all the parameters    
    answer = raw_input("do you want to use the default values? \n exit = 1 \n pitfall = -1 \n reward = -0.04 \n gamma = 0.9 \n (y)/(n)? ")
    if(answer=="y"):
        exit_value = 1
        pitfall_value = -1
        reward_value = -0.04
        discount_value = 0.9
    else:
        discount_value = -1.0
        while discount_value < 0 or discount > 1.0:
            try:
                discount_value = float(raw_input("Please define a discount-value between 0 and 1: "))
            except ValueError:
                print("Oh noes! you typed in a wrong number!!! please try a number between 0 and 1: ")
        reward_value = 1
        while reward_value > 0:
            try:
                reward_value = float(raw_input("Please define a reward < 0: "))
            except ValueError:
                print("Oh noes! you typed in a wrong number!!! please try a number < 0: ")
        #possibly add the settings of the other values

    problem = mdp(grid, exit_value, pitfall_value, reward_value, discount_value)
    return problem


#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - M A I N - - - - - - - - - - - - - - - - - - - -    
def __MAIN__():
    problem = initalize()
    terminate = True
    print("_ _ _ _ _ _ _ _ _ _ _ O P T I O N S _ _ _ _ _ _ _ _ _ _ _")
    print("Iterate once and print reward matrix: [1]")
    print("update policy and print: [2]")
    print("Iterate reward matrix n times and update policy matrix, print both: [3]")
    print("print structure matrix: [4]")
    print("print current reward matrix: [5]")
    print("print current policy matrix: [6]")
    print("terminate program: [7]")
    print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
    while terminate:
        command = -1
        while command > 7 or command < 1:
            try:
                command = int(raw_input("Please select an option: "))
            except ValueError:
                print
        if command == 1:
            #problem.update_values()
            problem.policy_evaluation()
            print(problem.value_matrix)

        if command == 2:
            #problem.update_policy()
            problem.policy_update()
            print(problem.policy)
        if command == 3:
            times = int(raw_input("Please specify the number of steps to be evaluated: "))
            while times != 0:
                problem.policy_evaluation()
                times -= 1
            #problem.update_policy()
            problem.policy_update
            print(problem.value_matrix)
            print(problem.policy)
        if command == 4:
            print(problem.structure_mat)
        if command == 5:
            print(problem.value_matrix)
        if command == 6:
            print(problem.policy)
        if command == 7:
            terminate = False
            print("Goodbye!")
            
        
        
    
    
    
    
    
    
    
    

    
    
__MAIN__()