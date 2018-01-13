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
            problem.update_values()
            print(problem.value_matrix)
        if command == 2:
            problem.update_policy()
            print(problem.policy)
        if command == 3:
            times = int(raw_input("Please specify the number of steps to be evaluated: "))
            while times != 0:
                problem.update_values()
                times -= 1
            problem.update_policy()
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