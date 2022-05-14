#HOMEWORK ASSIGNMENT 2 CODING
#ARTIFICIAL INTELLIGENCE
#DONGBING HAN/dh3071
#2021.10.2

from __future__ import division
from __future__ import print_function

import heapq
import resource
import sys
import math
import time
import queue as Q


#### SKELETON CODE ####
## The Class that Represents the Puzzle
from typing import List, Union, Any, Type


class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    # depth = 0


    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n * n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n * n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.config = config
        self.children = []


        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

        # if self.parent is not None:
        #     self.depth = parent.depth + 1
        # else:
        #     self.depth = 0

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3 * i: 3 * (i + 1)])

    def move_up(self):
        """
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """

        new_lst = self.config[:]
        pos = self.config.index(0)
        if pos in [0, 1, 2]:
            return None
        else:
            temp = new_lst[pos]
            new_lst[pos] =  new_lst[pos - 3]
            new_lst[pos - 3] = temp
            return PuzzleState(new_lst, self.n, self, "Up", (self.cost + 1))


    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """

        new_lst = self.config[:]
        pos = self.config.index(0)
        if pos in [6, 7, 8]:
            return None
        else:
            temp = new_lst[pos]
            new_lst[pos] = new_lst[pos + 3]
            new_lst[pos + 3] = temp
            return PuzzleState(new_lst, self.n, self, "Down", (self.cost + 1))



    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """

        new_lst = self.config[:]
        pos = self.config.index(0)
        if pos in [0, 3, 6]:
            return None
        else:
            temp = new_lst[pos]
            new_lst[pos] =  new_lst[pos - 1]
            new_lst[pos - 1] = temp
            return PuzzleState(new_lst, self.n, self, "Left", (self.cost + 1))



    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        new_lst = self.config[:]
        pos = self.config.index(0)
        if pos in [2, 5, 8]:
            return None
        else:
            temp = new_lst[pos]
            new_lst[pos] =  new_lst[pos + 1]
            new_lst[pos + 1] = temp
            return PuzzleState(new_lst, self.n, self, "Right", (self.cost + 1))


    def expand(self):
        """ Generate the child nodes of this node """

        # Node has already been expanded
        if len(self.children) != 0:
            return self.children

        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()
        ]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]

        return self.children


# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(curnode, max, expand, rumtime):
    ### Student Code Goes here
    
    curcost = curnode.cost

    path = [curnode.action]
    while curnode.parent is not None:
        parent = curnode.parent
        path.append(parent.action)
        curnode = parent

    path.reverse()
    path.pop(0)
    ramtime = rumtime

    end_rusage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
  


    f = open("output.txt", "w")
    f.write("path_to_goal: " + str(path) + '\n')
    f.write("cost_of_path: " + str(curcost) + '\n')
    f.write("nodes_expanded: " + str(expand) + '\n')
    f.write("search_depth: " + str(curcost) + '\n')
    f.write("max_search_depth: " + str(max) + '\n')
    f.write("running_time: " + str(ramtime) + '\n')
    f.write("max_ram_usage: " + str(end_rusage * 0.00000001) + '\n')
    f.close()

    pass



def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    start_time = time.time()
    frontier = Q.Queue()
    froconfig = set()
    frontier.put(initial_state)
    explored = set()
    nodes_expands = 0
    maxdepth = 0

    while not frontier.empty():
        curnode = frontier.get()
        explored.add(tuple(curnode.config))
        maxdepth = curnode.cost
        # curnode.depth = maxdepth + 1

        if test_goal(curnode):
            end_time = time.time()
            writeOutput(curnode, maxdepth+1, nodes_expands, end_time - start_time)
            return


        nodes_expands = nodes_expands + 1
        neighbors = curnode.expand()
        for neighbor in neighbors:
            #if neighbor not in frontier.queue and tuple(neighbor.config) not in explored:
            if tuple(neighbor.config) not in froconfig and tuple(neighbor.config) not in explored:
                # maxdepth = max(maxdepth,neighbor.cost)
                frontier.put(neighbor)
                froconfig.add(tuple(neighbor.config))
                explored.add(tuple(neighbor.config))






def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    start_time = time.time()
    frontier = []
    frontier.append(initial_state)
    froconfig = set()
    explored = set()
    nodes_expands = 0
    maxdepth = 0

    while not frontier == []:
        curnode = frontier.pop()
        explored.add(tuple(curnode.config))
        # curnode.depth = maxdepth

        if test_goal(curnode):
            end_time = time.time()
            writeOutput(curnode, maxdepth, nodes_expands, end_time - start_time)
            return

        nodes_expands = nodes_expands + 1
        neighbors = curnode.expand()
        neighbors.reverse()
        for neighbor in neighbors:
            if tuple(neighbor.config) not in explored and tuple(neighbor.config) not in froconfig :
                maxdepth = max(maxdepth, neighbor.cost)
                frontier.append(neighbor)
                froconfig.add(tuple(neighbor.config))
                explored.add(tuple(neighbor.config))
                



def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    start_time = time.time()
    frontier = []
    froconfig = set()
    explored = set()
    entry = 0
    heapq.heappush(frontier, (calculate_total_cost(initial_state), entry, initial_state))
    nodes_expands = 0
    maxdepth = 0

    while not frontier == []:
          curnode = heapq.heappop(frontier)[2]
          explored.add(tuple(curnode.config))
          maxdepth = curnode.cost
          # curnode.depth = maxdepth

          if test_goal(curnode):
              end_time = time.time()
              writeOutput(curnode, maxdepth, nodes_expands, end_time - start_time)
              return

          nodes_expands = nodes_expands+1
          neighbors = curnode.expand()
          for neighbor in neighbors:
              if tuple(neighbor.config) not in froconfig and tuple(neighbor.config) not in explored:
                  entry = entry +1
                  froconfig.add(tuple(neighbor.config))
                  explored.add(tuple(neighbor.config))
                  heapq.heappush(frontier, (calculate_total_cost(neighbor), entry, neighbor))



def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###

    configlst = state.config
    cost = state.cost
    curcost = 0

    for value in range(1,9):
        curindex = configlst.index(value)
        curManhattan = calculate_manhattan_dist(curindex, value, 3)
        curcost = curcost + curManhattan

    return curcost + cost


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    #global curx,cury,golx,goly,golindex
    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    goalindex = goal.index(value)
    # print("goal index: ")
    # print(goalindex)
    # print("\n")


    if idx  == [0,3,6]:
        #print("check 1 \n")
        curx = 0
        cury = int(idx / n)
        # print(curx)
        # print(cury)
        # print("\n")
    else:
        #print("check 2 \n")
        curx = int(idx % n)
        cury = int(idx / n)
        # print(curx)
        # print(cury)
        # print("\n")

    if goalindex ==[0,3,6]:
        #print("check 3 \n")
        golx = 0
        goly = int(goalindex / n)
        # print(golx)
        # print(goly)
        # print("\n")
    else:
        # print("check 4")
        golx = int(goalindex % n)
        # print(golx)
        goly = int(goalindex / n)
        # print(goly)
        # print("\n")

    return abs(golx - curx) + abs(goly - cury)

    pass


def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    # cur_state = puzzle_state
    goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    if puzzle_state.config == goal_state:
        return 1
    else:
        return 0

    pass


# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, board_size)
    start_time = time.time()


    if search_mode == "bfs":
        bfs_search(hard_state)

    elif search_mode == "dfs":
        dfs_search(hard_state)

    elif search_mode == "ast":
        A_star_search(hard_state)

    else:
        print("Enter valid command arguments !")

    end_time = time.time()
    print("Program completed in %.3f second(s)" % (end_time - start_time))

if __name__ == '__main__':
    main()