# Prepare the Bunnies' Escape
# ===========================

# You're awfully close to destroying the LAMBCHOP doomsday device and freeing Commander 
# Lambda's bunny workers, but once they're free of the work duties the bunnies are going to 
# need to escape Lambda's space station via the escape pods as quickly as possible. 
# Unfortunately, the halls of the space station are a maze of corridors and dead ends 
# that will be a deathtrap for the escaping bunnies. Fortunately, Commander Lambda has 
# put you in charge of a remodeling project that will give you the opportunity to make 
# things a little easier for the bunnies. Unfortunately (again), you can't just remove 
# all obstacles between the bunnies and the escape pods - at most you can remove one wall 
# per escape pod path, both to maintain structural integrity of the station and to avoid 
# arousing Commander Lambda's suspicions. 

# You have maps of parts of the space station, each starting at a work area exit and 
# ending at the door to an escape pod. The map is represented as a matrix of 0s and 1s, 
# where 0s are passable space and 1s are impassable walls. The door out of the station is 
# at the top left (0,0) and the door into an escape pod is at the bottom right (w-1,h-1). 

# Write a function solution(map) that generates the length of the shortest path from the 
# station door to the escape pod, where you are allowed to remove one wall as part of 
# your remodeling plans. The path length is the total number of nodes you pass through, 
# counting both the entrance and exit nodes. The starting and ending positions are 
# always passable (0). The map will always be solvable, though you may or may not 
# need to remove a wall. The height and width of the map can be from 2 to 20. Moves can 
# only be made in cardinal directions; no diagonal moves are allowed.

# Languages
# =========

# To provide a Python solution, edit solution.py
# To provide a Java solution, edit Solution.java

# Test cases
# ==========
# Your code should pass the following test cases.
# Note that it may also be run against hidden test cases not shown here.

# -- Python cases --
# Input:
# solution.solution(
# [[0, 1, 1, 0], 
#  [0, 0, 0, 1], 
#  [1, 1, 0, 0], 
#  [1, 1, 1, 0]])
# Output:
#     7

# Input:
# solution.solution(
# [[0, 0, 0, 0, 0, 0], 
#  [1, 1, 1, 1, 1, 0], 
#  [0, 0, 0, 0, 0, 0], 
#  [0, 1, 1, 1, 1, 1], 
#  [0, 1, 1, 1, 1, 1], 
#  [0, 0, 0, 0, 0, 0]])
# Output:
#     11

from copy import deepcopy
from pprint import pprint
from Queue import PriorityQueue


class State(object):
    def __init__(self, value, parent, start = (0, 0), goal = (0, 0)):
        self.children = []
        self.parent = parent
        self.value = value
        self.dist = 0
        if parent:
            self.path = parent.path[:]
            self.path.append(value)
            self.start = parent.start
            self.goal = parent.goal
        else:
            self.path = [value]
            self.start = start
            self.goal = goal

    def get_distance(self, h_func):
        return h_func(self.start, self.goal)

    def create_children(self, map, h_func):
        x = self.value[0]
        y = self.value[1]

        up = (x, y + 1)
        down = (x, y - 1)
        right = (x + 1, y)
        left = (x - 1, y)

        if x - 1 >= 0 and map[x-1][y] == 0:
            h_func()




def wall_can_be_deleted(map, x, y):
    counter = 0
    if x + 1 < len(map) and map[x + 1][y] == 1:
        counter += 1
    if x - 1 >= 0 and map[x - 1][y] == 1:
        counter += 1
    if y + 1 < len(map) and map[x][y + 1] == 1:
        counter += 1
    if y - 1 >= 0 and map[x][y - 1] == 1:
        counter += 1
    
    if (x == 0 or 
        x == len(map) -1 or 
        y == 0 or 
        y == len(map) - 1) and counter < 1:
        return True
    elif (x == 0 or 
          x == len(map) -1 or 
          y == 0 or 
          y == len(map) - 1) and counter < 2:
        return True
    return False


def walls_can_be_deleted(map):
    deletable_walls = deepcopy(map)
    for index_x in range(len(map)):
        for index_y in range(len(map)):
            if (map[index_x][index_y] == 1 and 
                wall_can_be_deleted(map, index_x, index_y)):
                deletable_walls[index_x][index_y] = 1
            else:
                deletable_walls[index_x][index_y] = 0
    return deletable_walls


def heuristic(start, goal):
    x_0 = start[0]
    y_0 = start[1]
    x_1 = goal[0]
    y_1 = goal[1]
    return (abs(x_0 - x_1) + abs(y_0 - y_1))


def generate_map_variations(map):
    map_copy = deepcopy(map)
    map_variations = []
    map_variations.append(map_copy)
    deletable_walls = walls_can_be_deleted(map_copy)

    for index_x in range(len(map_copy)):
        for index_y in range(len(map_copy)):
            if (map_copy[index_x][index_y] == 1 
                and deletable_walls[index_x][index_y] == 1):
                new_map_variation = deepcopy(map_copy)
                new_map_variation[index_x][index_y] = 0
                map_variations.append(new_map_variation)         
    return map_variations


def a_star(map, start, goal):
    for x in range(len(map)):
        for y in range(len(map)):
            node = (x, y)
            node_val = map[x][y]



def solution(map):
    map_vars = generate_map_variations(map)
    path_lenghts = []
    goal = (len(map) - 1, len(map) - 1)

    for map in map_vars:
        path_lenghts.append(a_star(map, (0, 0), goal))  

    # TODO - shortest path sorting


map = [
    [0, 0, 0, 0, 0, 0], 
    [1, 1, 1, 1, 1, 0], 
    [0, 0, 0, 0, 0, 0], 
    [0, 1, 1, 1, 1, 1], 
    [0, 1, 1, 1, 1, 1], 
    [0, 0, 0, 0, 0, 0]]

solution(map)
