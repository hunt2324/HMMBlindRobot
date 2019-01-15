from Maze import Maze
from time import sleep

class SensorlessProblem:

    ## You write the good stuff here:
    def __init__(self, maze):
        self.maze = maze
        self.start_state = self.generate_intial() # #gives access to start state through out the maze

    def __str__(self):
        string =  "Blind robot problem: "
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

    def is_goal(self, state): # test if it is a singleton
        return len(state) == 1

    def cardinality_heuristic(self,state): # heurstic to test the cardinality of the state
        cardinality = len(state)

        return cardinality

    def get_walls(self): # did not use
        walls = []
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                if not self.maze.is_floor(x,y):
                    # spot is wall
                    walls.append(x)
                    walls.append(y)

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

    def get_successors(self, possible_states):
        successors_list = [] # list for the succesors
        # iterate through each action
        for action in self.get_actions():
            print("action:\n")
            print(action)

            successor_belief_set = set()
            print("possible states:")
            print(possible_states)
            for state in possible_states: # iterate through each possible state
                # run action on state
                new_state_x = state[0] + action[0]
                new_state_y = state[1] + action[1]
                if self.is_action_legal(new_state_x, new_state_y): # if its a legal action i can just add them becuase the set will not acceot duplicates
                    successor_belief_set.add((new_state_x,new_state_y)) # add a tuple of every leagal state for the action ignoring duplicates
                else: # don't want to lose the previous state just becuase the new one is illegal so addd it to the set
                    successor_belief_set.add(state)
                    #add the state set to the list of succesors

            successors_list.append(frozenset(successor_belief_set)) # add the generated successors to the list


        return successors_list

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state)
        print(self.maze.robotloc)

        for state in path:
            print(str(self))
            temp = [i for tup in state for i in tup]
            self.maze.robotloc = tuple(temp)
            sleep(1)

            print(str(self.maze))


## A bit of test code

if __name__ == "__main__":
    test_maze1 = Maze("maze1.maz")
    test_problem = SensorlessProblem(test_maze1)
    # testing my methods
    intial = test_problem.generate_intial()
    test_problem.get_successors(frozenset({(3, 1), (1, 1), (2, 2)})) # just some test code
