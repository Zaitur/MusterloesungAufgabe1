import numpy as np


grid1 = np.genfromtxt("3by4.grid",dtype='str')
grid2 = np.genfromtxt("5by10.grid",dtype='str')
grid3 = np.genfromtxt("9by17.grid",dtype='str')

#now come all the functions - yay

def state_transition_prob(x,y,_x,_y, action):
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
        if(action=="D"):
            return 0.8
        if(action=="L" or action=="R"):
            return 0.1
        
    if(delta_x<0):
        #We want to move up
        if(action=="U"):
            return 0.8
        if(action=="L" or action=="R"):
            return 0.1
        
    if(delta_y>0):
        #We want to move right
        if(action=="R"):
            return 0.8
        if(action=="U" or action=="D"):
            return 0.1
        
    if(delta_y<0):
        #We want to move left
        if(action=="L"):
            return 0.8
        if(action=="U" or action=="D"):
            return 0.1
        
    #case that we want to find the probability to stay in original state:
    #here we need to check whether the neighbouring cells, where we could end up if doing action 
    #"action" are actually obstacles. If that is the case, it increases the probability that we stay where we are
    if(delta_x==0 and delta_y==0):
        prob = 0
        if(action=="R"):
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

        if(action=="D"):
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

        if(action=="L"):
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

        if(action=="U"):
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
def reward(x,y, action):
    if(grid[x][y]=="F"):
        #existance is pain... just moving gives us the "reward" of the penalty that the user has set
        return value_penalty
    if(grid[x][y]=="E"):
        return 1
    if(grid[x][y]=="P"):
        return -1
    return 0

# one step of the policy evaluation
def policy_evaluation(policy_matrix, value_matrix):
    values = np.zeros(grid.shape)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            
            if(grid[i][j]=="E"): #value of the cell with the exit, should not change
                values[i][j]=value_goal
            elif(grid[i][j]=="P"): # same with pitfall
                values[i][j]=value_pitfall
            else:
                #see slide 40 for algorithm
                # the new value for a cell is the current reward in the cell (so mostly the movement penalty)
                # plus the probality to end up in a neighbouring cell * the reward of that cell
                # for each cell that we could end up in, given our current policy matrix
                values[i][j]= reward(i,j, policy_matrix[i][j])+value_gamma*policy_evaluation_helper(i,j,policy_matrix[i][j], value_matrix)
    return values

#this is just a part of the algorithm on slide 40
def policy_evaluation_helper(x,y, action, value_matrix):
    summe = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            summe += state_transition_prob(x,y,i,j, action)*value_matrix[i][j]
    return summe

#here we want to change the policy
# see slide 49 for algorithm
def policy_update(policy_matrix, value_matrix):
    _policies = policy_matrix
    for i in range(len(grid)):
        for j in range(len(grid[0])):
                # for each cell we want to check which action would give us the best result
                maximum = 0
                policy = "R"
                for action in ["U","D","R","L"]:
                    new = reward(i,j, action) + value_gamma*policy_evaluation_helper(i,j, action, value_matrix)
                    print(new)
                    if (new > maximum): 
                        maximum = new
                        policy = action
                _policies[i][j] = policy
    return _policies

# do policy evaluation until it converges (the bellmann criterion is fulfilled)
def automatic_policy_evaluation(policy_matrix, value_matrix):
    bellmann = False
    steps = 0
    values = value_matrix
    while(bellmann == False):
        value_matrix_before = values
        values = policy_evaluation(policy_matrix, values)
        steps += 1
        difference = value_matrix_before-values
        #print(difference)
        bellmann = np.all(np.array([i for i in np.all(abs(i)<0.01 for i in (difference))]))
    print("it took "+str(steps)+" steps until the iterative policy evaluation converged")
    return values

    #do the whole shizzely-dizzely until everything converges (see slide 50)
def automatic_policy_iteration(policy_matrix, value_matrix):
    steps = 0
    values = value_matrix
    policies = policy_matrix
    bellmann = False
    while(bellmann == False):
        # we do policy evaluation until it converges
        values = automatic_policy_evaluation(policies, values)
        policy_matrix_before = np.array(policies)
        #then we update our policy
        policies = policy_update(policies, values)
        #and we do that until the policy matrix does not change anymore
        no_change = np.all(policy_matrix_before == policies)
        if(no_change == True):
            bellmann = True
        steps += 1
    print("final values: ")
    print(values)
    print("final policy: ")
    print(policies)
    print("it took "+str(steps)+" steps to do this shit")


#User Dialogue
while True:
    try:
        grid_choice = int(input("oh boi! Seems like we have some calculations to do! I have a 3by4 matrix, a 5by10 matrix and a 9by17 matrix to offer. Please indicate your choice by typing 1, 2 or 3: "))
        if (grid_choice >3 or grid_choice < 1): 
            raise ValueError
        
        break
    except ValueError:
        print("Oh noes! you typed in a wrong number!!! please try a number between 1 and 3: ")

        
while True:
    try:
        value_goal = int(input("Next, please tell me the value of the goal: "))
        if (value_goal<0): 
            raise ValueError 
        value_pitfall = int(input("Next, please tell me the value of the pitfall: "))
        if (value_pitfall>0): 
            raise ValueError 
            
        value_penalty = float(input("Next, please tell me the value of the movement penalty: "))
        if (value_penalty >0): 
            raise ValueError 
            
        value_gamma = float(input("Next, please tell me the value of gamma: "))
        if (value_gamma<0 or value_gamma >1): 
            raise ValueError 
        break
    except ValueError:
        print("Oh noes! you typed in a wrong number!!! ")        
        
        
        
while True:
    try:
        calc_choice = int(input("Next, please choose whether you want to calculate yourself, or let me do it automatically by typing 1 or 2: "))
        if (calc_choice >2 or calc_choice < 1): 
            raise ValueError
        
        break
    except ValueError:
        print("Oh noes! you typed in a wrong number!!! please type either 1 or 2: ")

        
 

       
        
        
#storing the grid that the user selected
if (grid_choice == 1):
    grid = grid1
elif (grid_choice == 2):
    grid = grid2
else:
    grid = grid3

#initializing the value matrix first with zeroes and the pitfall/exit values 
value_matrix = np.zeros(grid.shape)

for i in range(len(grid)):
    for j in range(len(grid[0])):
        if(grid[i][j]=="O"):
            value_matrix[i][j]= 0   #obstacle gets value zero, could also be something else?
        elif(grid[i][j]=="E"):
            value_matrix[i][j]= value_goal
        elif(grid[i][j]=="P"):
            value_matrix[i][j]= value_pitfall

# initializing the policy_matrix with all right-moves
policy_matrix = np.zeros(grid.shape)
policy_matrix = policy_matrix.astype("str")
policy_matrix[policy_matrix=="0.0"] = "R"


if(calc_choice==2):
    print("this is the grid:")
    print(grid)
    automatic_policy_iteration(policy_matrix, value_matrix)
else:
    jo = "ja"
    while (jo != "no" ):
        jo = input("what step should I do? possible answers: evaluation, automatic, update")
        if(jo == "evaluation"):
            value_matrix = policy_evaluation(policy_matrix, value_matrix)
            print(value_matrix)
        if(jo == "automatic"):
            value_matrix = automatic_policy_evaluation(policy_matrix, value_matrix)
            print(value_matrix)
        if(jo == "update"):
            policy_matrix = policy_update(policy_matrix, value_matrix)
            print(policy_matrix)
    print("thanks")
