from Maze_HMM import Maze
from time import sleep
import random
import numpy as np
import CantorPairing
class HMM:

    ## You write the good stuff here:
    def __init__(self, maze):
        self.maze = maze
        self.start_states = self.generate_intial() # #gives access to start state through out the maze
        #self.sensor_model
        self.path =[]
        self.sensor_model = self.generate_sensor_models()
        self.transition_model = self.get_transition_model()

    def __str__(self):
        string =  "HMM robot problem: "
        return string

        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def get_actions(self):  # get all the actions posssible
        return [#(0, 0),  # don't move
                (0, 1),  # go north
                (1, 0),  # go east
                (-1, 0),  # go west
                (0, -1)  # go south
                ]

    def generate_sensor_models(self):
        """ generates sensor model as   a 3d matrix 
            to save computation time and so that i 
            can return the entire model"""
        possible_states = self.generate_intial()
        #print(possible_states)
        sensor_model  = np.zeros((4, 16, 16))
        colors = ['R', 'B', 'G', 'Y']
        for state in possible_states:
            for color in colors:
                if self.maze.get_color(state[0], state[1]) == color:
                    sensor_model[colors.index(color), self.maze.index(state[0], state[1]), self.maze.index(state[0], state[1])] = .88
                else:
                    sensor_model[colors.index(color), self.maze.index(state[0], state[1]), self.maze.index(state[0], state[1])] = .04
        #print(sensor_model[0,self.maze.index(2,3),self.maze.index(2,3)])
        return sensor_model

    def get_transition_model(self):
        """generate a transition model"""
        possible_states = self.generate_intial() # get the possible states
        trans_model = np.zeros((16, 16)) # 16X16 matrix
        for state in possible_states: # go through all possible states

            possible_moves = self.get_successors(state)
            num_moves = len(possible_moves)
            for new_state in possible_moves:
                # add the probability of that state moving to the next state to the transition matrix
                # will add higher than .25 probablity if it stays on the same state for some of the possible moves
                trans_model[self.maze.index(state[0], state[1]), self.maze.index(new_state[0], new_state[1])] = possible_moves.count(new_state) * .25
        return trans_model

    def forward_condition(self): # intial forward condition ( all values have a 1/16th chance)
        a = np.empty(( 16, 1));
        a.fill(1/16)
        return a


    def is_action_legal(self, new_x, new_y):
        if not self.maze.is_floor(new_x, new_y):
            return False
        return True

    def generate_intial(self): ## generates the intial state
        #look through the maze and generate the list of intial start values
        initial_states = []
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                if self.maze.is_floor(x,y): # for all square in the maze test if they are a floor if they are add them to the intial states
                    #available spot
                    initial_states.append((x,y))
        return(frozenset(initial_states)) # return a frozen set

    def get_successors(self, state):
        successors_list = [] # list for the succesors
        # iterate through each action
        for action in self.get_actions():
            #print("action:\n")
            #print(action)


            new_state_x = state[0] + action[0]
            new_state_y = state[1] + action[1]
            if self.is_action_legal(new_state_x, new_state_y): # if its a legal action i can just add them becuase the set will not acceot duplicates
                successors_list.append((new_state_x,new_state_y)) # add a tuple of every leagal state for the action ignoring duplicates
            else: # don't want to lose the previous state just becuase the new one is illegal so addd it to the set
                successors_list.append(state)
                #add the state state to the list of successors
        #print("got here")
        #print(successors_list)
        return successors_list

    def solver(self, forward, sensor_evidence, count=0): # solves using HMM filtering
        print("Step " + str(count) + ":")
        print_solution(normalize(forward))

        if len(sensor_evidence) == 0: ## base case for recursion
            #print(forward)
            return forward



        # pick sensor model picks the sensor model based on what the reading from the sensor is
        reading  =  sensor_evidence[0]
        if reading == 'R':
            guessed_model = self.sensor_model[0, :, :]
        if reading == 'B':
            guessed_model = self.sensor_model[1, :, :]
        if reading == 'G':
            guessed_model = self.sensor_model[2, :, :]
        if reading == 'Y':
            guessed_model = self.sensor_model[3, :, :]


        tranposed_model = np.transpose(self.transition_model)
        temp = np.matmul(tranposed_model, forward)
        forward = np.matmul(guessed_model, temp)
        return self.solver(forward, sensor_evidence[1:], count+1) # recurse

def normalize(array): # normalize at the end
    _sum = np.sum(array)

    return np.divide(array, _sum)


def print_solution(solution): # prints the solution like the board for displaying
    count = 0
    for i in solution:
        #print(i)
        print("%3.3f" % i[0], end="\t")
        if count % 4 == 3:
            print()
        count += 1


def get_sensor_reading_path(correct_path): # generates a faulty path based on the sensors probablity of falure given the correct path
    colors = ['R', 'G', 'Y', 'B']
    faulty_path = []
    for color in correct_path:
        n = random.randint(1,100)
        if n > 84:
            i = random.randint(0,3)
            faulty_path.append(colors[i])
        else:
            faulty_path.append(color)
    return faulty_path


## A bit of test code

if __name__ == "__main__":
    filename = "maze1.maz"
    test_maze = Maze(filename)
    test_problem = HMM(test_maze)
    test_problem.generate_sensor_models()
    test_problem.get_transition_model()

    correct_paths = []
    if filename == "maze1.maz":
        correct_paths = [['B', 'R', 'B', 'G', 'Y'],
                         ['Y', 'Y', 'G', 'R', 'G', 'B', 'R', 'B'],
                         ['B', 'G', 'Y', 'G', 'R', 'G', 'B', 'R', 'B', 'G', 'Y', 'Y']]
    elif filename == "maze2.maz":
        correct_paths = [['B', 'R', 'Y', 'B', 'R', 'G'],
                         ['G', 'R', 'B', 'Y', 'R', 'Y', 'B']]
    elif filename == "maze3.maz":
        correct_paths = [['Y','B', 'G', 'Y', 'G','R','R','R' ,'Y','B','B']]


    # Test 1 with a correct path
    for correct_path in correct_paths:
        print("Solver ran on the correct path:")
        print(correct_path)
        solution = test_problem.solver(test_problem.forward_condition(), correct_path)
        # faulty path test
        print("Solver ran on the sensor reading simulated path :")
        sensor_reading_path = get_sensor_reading_path(correct_path)
        print(sensor_reading_path)
        solution = test_problem.solver(test_problem.forward_condition(), sensor_reading_path)

