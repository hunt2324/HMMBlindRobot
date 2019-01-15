from Maze import Maze
from time import sleep

class MazeworldProblem:

    ## you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations):
        self.maze = maze
        self.goal_locations = goal_locations
        self.start_state = tuple([0] + list(self.maze.robotloc))

    def __str__(self):
        string = "Mazeworld problem: "
        return string

    # TODO
    def manhattan_heuristic(self, state): # this is just the basic manhattan heurstic
        working_state = state[1:]
        robot_turn = state[0]

        robot_x = working_state[robot_turn * 2]
        robot_y = working_state[robot_turn * 2 + 1]
        goal_x = self.goal_locations[robot_turn * 2]
        goal_y = self.goal_locations[robot_turn * 2 + 1]
        x_dist = abs(robot_x - goal_x)
        y_dist = abs(robot_y - goal_y)

        return (x_dist + y_dist)


    # given a sequence of states (including robot turn), modify the maze and print it out.
    #  (Be careful, this does modify the maze!)
    def is_goal(self, state):
        return self.goal_locations == state[1:] # if the robot has reached the goal state given return true

    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[1:])

        for state in path:
            print(str(self))
            self.maze.robotloc = tuple(state[1:])
            #sleep(1)

            print(str(self.maze))

    def get_actions(self): #
        return [(0,0),  # don't move
                (0,1),  # go north
                (1,0),  # go east
                (-1,0),  # go west
                (0, -1)  # go south
                ]

    def is_action_legal(self, new_x, new_y): # test if the actions are leagal
        if self.maze.has_robot(new_x, new_y): # don't overlap robots
            return False
        if not self.maze.is_floor(new_x, new_y): # don't move into a wall or of the board
            return False
        return True

    def get_successors(self, state): # finds the successors of a state
        self.maze.robotloc = state[1:]
        #rint(self.maze.robotloc)
        robot_turn = state[0]

        robot_x = self.maze.robotloc[robot_turn*2] # gets the x and y using the robots turn to find it in the tuple
        robot_y = self.maze.robotloc[robot_turn*2+1]

        successors = []
        #print("Actions: " + str(self.get_actions()))
        for action in self.get_actions(): # runs through each action
            new_robot_x = robot_x + action[0]
            new_robot_y = robot_y + action[1]
            if new_robot_x == robot_x and new_robot_y == robot_y: # if the robot has not moved there is no point in checking if it is legal ( saves a small number of operation
                new_state = list(state)
                new_state[0] = (robot_turn + 1) % int((len(state) / 2))
                successors.append(tuple(new_state)) # add the state to the list of succesors

            # check if action legal
            elif self.is_action_legal(new_robot_x, new_robot_y): # checks the legality of the move
                # add to successors
                new_state = list(state)
                new_state[0] = (robot_turn + 1) % int((len(state) / 2)) # switching the turn
                new_state[robot_turn*2+1] = new_robot_x
                new_state[robot_turn*2+2] = new_robot_y
                successors.append(tuple(new_state)) # add to the succesors


        return successors


## A bit of test code. You might want to add to it to verify that things
#  work as expected.

if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

    #print(test_mp.get_successors((0, 1, 0, 1, 2, 2, 1)))
    print(" 2, 1, 0, 1, 2, 2, 1")
    print(test_mp.get_successors((2, 1, 0, 1, 2, 2, 1)))
    #print(test_mp.get_successors((1, 1, 1, 1, 2, 2, 1)))