# You write this:

from SensorlessProblem import SensorlessProblem
from Maze_blind import Maze

#from uninformed_search import bfs_search
from astar_search import astar_search

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0

#  NOTE the huerstic i used can be fount in the SensorlessProblem.py
# Test on all the mazes given
test_maze3 = Maze("maze3.maz")
test_mp = SensorlessProblem(test_maze3)

result = astar_search(test_mp, null_heuristic)
print(result)
test_mp.animate_path(result.path)
print(result)

result = astar_search(test_mp, test_mp.cardinality_heuristic)
print(result)
test_mp.animate_path(result.path)
print(result)

test_maze1 = Maze("maze1.maz")
test_mp = SensorlessProblem(test_maze1)

result = astar_search(test_mp, test_mp.cardinality_heuristic)
print(result)
test_mp.animate_path(result.path)
print(result)

test_maze2 = Maze("maze2.maz")
test_mp = SensorlessProblem(test_maze2)

result = astar_search(test_mp, test_mp.cardinality_heuristic)
print(result)
test_mp.animate_path(result.path)
print(result)

