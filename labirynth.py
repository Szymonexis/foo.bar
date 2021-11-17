from copy import deepcopy
from Queue import PriorityQueue
from pprint import pprint


def wall_can_be_deleted(map, x, y):
    counter = 0
    if x + 1 < len(map) and map[x + 1][y] == 1:
        counter += 1
    if x - 1 >= 0 and map[x - 1][y] == 1:
        counter += 1
    if y + 1 < len(map[0]) and map[x][y + 1] == 1:
        counter += 1
    if y - 1 >= 0 and map[x][y - 1] == 1:
        counter += 1
    
    if counter < 3:
        return True
    return False


def walls_can_be_deleted(map):
    deletable_walls = deepcopy(map)
    for index_x in range(len(map)):
        for index_y in range(len(map[0])):
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
        for index_y in range(len(map_copy[0])):
            if (map_copy[index_x][index_y] == 1 
                and deletable_walls[index_x][index_y] == 1):
                new_map_variation = deepcopy(map_copy)
                new_map_variation[index_x][index_y] = 0
                map_variations.append(new_map_variation)     
    return map_variations


def h(node, goal):
    return (abs(node[0] - goal[0]) +
            abs(node[1] - goal[1]))


def get_neighbors(node, map):
    neighbors = []

    x = node[0]
    y = node[1]

    up = (x, y - 1)
    down = (x, y + 1)
    left = (x - 1, y)
    right = (x + 1, y)

    # up
    if y - 1 >= 0 and map[up[0]][up[1]] == 0:
        neighbors.append(up)
    # down
    if y + 1 < len(map[0]) and map[down[0]][down[1]] == 0:
        neighbors.append(down)
    # left
    if x - 1 >= 0 and map[left[0]][left[1]] == 0:
        neighbors.append(left)
    # right
    if x + 1 < len(map) and map[right[0]][right[1]] == 0:
        neighbors.append(right)

    return neighbors


def get_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append((0, 0))
    return path


def algorithm(map, start, goal):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {(x, y): float("inf") for x in range(len(map)) for y in range(len(map[0]))}
    g_score[start] = 0
    f_score = {(x, y): float("inf") for x in range(len(map)) for y in range(len(map[0]))}
    f_score[start] = h(start, goal)
    
    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == goal:
            return get_path(came_from, goal)
        
        for neighbor in get_neighbors(current, map):
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor, goal)
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

    return None


def solution(map):
    map_vars = generate_map_variations(map)
    path_lenghts = []
    start = (0, 0)
    goal = (len(map) - 1, len(map[0]) - 1)

    for map in map_vars:
        path = algorithm(map, start, goal)
        if path is not None:
            path_lenghts.append(len(path)) 

    shortest = path_lenghts[0]
    for path in path_lenghts:
        if path < shortest:
            shortest = path
    
    return shortest


map = [ [0, 1, 1, 0], 
        [0, 0, 0, 1], 
        [1, 1, 0, 0], 
        [1, 1, 1, 0]]

map_2 = [   [0, 0, 0, 0, 0, 0], 
            [1, 1, 1, 1, 1, 0], 
            [0, 0, 0, 0, 0, 0], 
            [0, 1, 1, 1, 1, 1], 
            [0, 1, 1, 1, 1, 1], 
            [0, 0, 0, 0, 0, 0]]

map_3 = [   [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 1, 1],
            [1, 1, 0, 0, 0],
            [0, 1, 0, 0, 0]]

pprint(solution(map_3))

