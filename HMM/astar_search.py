from SearchSolution import SearchSolution
from heapq import heappush, heappop, heapify
import timeit

class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object


    def __init__(self, state, heuristic, parent=None, transition_cost=0):

        # you write this part
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.transition_cost = transition_cost

    def priority(self):
        # you write this part
        return self.heuristic + self.transition_cost # the priority of the node is the transition cost plus the heurstic

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result


def find_node(pqueue, state): # not used
    for node in pqueue:
        if node.state == state:
            return node
    return None

def astar_search(search_problem, heuristic_fn):
    # I'll get you started:
    start = timeit.default_timer()
    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem.start_state))
    pqueue = []
    heappush(pqueue, start_node)

    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    visited_cost = {}
    visited_cost[start_node.state] = 0

    # you write the rest:
    while True: # start loop
        if len(pqueue) == 0: # if no solution is found just return the solution

            return solution
        node = heappop(pqueue) # pop a node off the pqueue
        solution.nodes_visited += 1
        if search_problem.is_goal(node.state):
            solution.path = backchain(node) # backchain from that node to find the path
            stop = timeit.default_timer() # runtime timer
            print(stop - start)
            solution.cost = node.transition_cost # set the cost "fuel" it took to get there to the transition cost of the last node
            return solution
        successors = search_problem.get_successors(node.state) # get the succesors the node
        #print(successors)
        for successor in successors: # run through the successors
            cost = 1
            if type(successor) is tuple and successor[1:] == node.state[1:]: # if the succesor is a tuple(multi robot problem) check if its the same as its parent node
                cost = 0 # if it is set the cost to 0
            child = AstarNode(successor, heuristic_fn(successor), node, node.transition_cost + cost) # create a child astar node with the new cost
            if child.state not in visited_cost.keys(): ## if it hasn't been visited add it to the pqueue and set the visted cost
                visited_cost[child.state] = child.transition_cost
                heappush(pqueue, child)
            elif child.transition_cost < visited_cost[child.state]: # else if the child has been visted but the new cost is lower
                #method runtime 0.09779066999908537 ## before hueristic added for multi robot problem

                visited_cost[child.state] = child.transition_cost # set the visted cost
                heappush(pqueue, child) # put it in the pqueue





















            #elif child.transition_cost < visited_cost[child.state]:
                # need to think about the time complexity given the building a heap is log n whereas iterating through the pqueue
                # time compexity is O(n) at worst

                #node_in_frontier = find_node(pqueue, child.state)
                #node_in_frontier.transaction_cost = child.transaction_cost
                #heapify(pqueue)
                # method runtime 09220100898528472 ## before hueristic added

            #else:
                #node_in_frontier = find_node(pqueue, child.state)
                #if node_in_frontier is not None and node_in_frontier.transaction_cost > child.transaction_cost:
                    #node_in_frontier.transaction_cost = child.transaction_cost
                    #heapify(pqueue)


