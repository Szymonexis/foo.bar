# Markhov chains - https://www.youtube.com/watch?v=bTeKu7WdbT8
# For example, consider the matrix m:
# [
#   [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
#   [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
#   [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
#   [0,0,0,0,0,0],  # s3 is terminal
#   [0,0,0,0,0,0],  # s4 is terminal
#   [0,0,0,0,0,0],  # s5 is terminal
# ]
# So, we can consider different paths to terminal states, such as:
# s0 -> s1 -> s3
# s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
# s0 -> s1 -> s0 -> s5
# Tracing the probabilities of each, we find that
# s2 has probability 0
# s3 has probability 3/14
# s4 has probability 1/7
# s5 has probability 9/14
# So, putting that together, and making a common denominator, gives an answer in the form of
# [s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
# [0, 3, 2, 9, 14].

# -- Python cases --
# Input:
# solution.solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]])
# Output:
#     [7, 6, 8, 21]

# Input:
# solution.solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
# Output:
#     [0, 3, 2, 9, 14]

import numpy as np
from fractions import gcd
from functools import reduce
from copy import deepcopy
from pprint import pprint

from numpy.lib.histograms import _search_sorted_inclusive


def transform_to_tuples(states):
    for x in range(len(states)):
        only_zeros = True
        sum = 0
        for element in states[x]:
            sum += element
            if element != 0:
                only_zeros = False
                break
        if only_zeros:
            for y in range(len(states[x])):
                if y == x:
                    states[x][y] = (1, 1)
                else:
                    states[x][y] = (0, 1)
        else:
            for y in range(len(states[x])):
                states[x][y] = (states[x][y], sum)
    return states


def populate_absorbing_states(states):
    for x in range(len(states)):
        only_zeros = True
        for element in states[x]:
            if element != 0:
                only_zeros = False
                break
        if only_zeros:
            for y in range(len(states[x])):
                if y == x:
                    states[x][y] = 1
    return states


def get_lcm(states):
    sums = []
    for line in states:
        sum = 0
        for value in line:
            sum += value
        sums.append(sum)

    absolute_multip = 1
    for sum in sums:
        absolute_multip = abs(absolute_multip * sum)
    return absolute_multip // reduce(gcd, sums)


def make_all_states_equal(states, lcm):
    for x in range(len(states)):
        sum = 0
        for y in range(len(states[x])):
            sum += states[x][y]
        multiply = lcm // sum
        for y in range(len(states[x])):
            states[x][y] *= multiply
    return states


def check_if_square(states):
    if len(states) != len(states[0]):
        return False
    return True


def standard_form(states, lcm, states_original):
    absorbing_states_indexes = []
    for x in range(len(states_original)):
        only_zeros = True
        for y in range(len(states_original[x])):
            if states_original[x][y] != 0:
                only_zeros = False
        absorbing_states_indexes.append(only_zeros)
    
    changes = [[(x, y) for y in range(len(states))] for x in range(len(states))]
    absorbing_states = []
    nonabsorbing_states = []

    for x in range(len(states)):
        if absorbing_states_indexes[x]:
            absorbing_states.append(states[x])
        else:
            nonabsorbing_states.append(states[x])
    absorbing_states_indexes = [value for value in absorbing_states_indexes if value]
    amount = len(absorbing_states_indexes)
    
    # TODO: set the matrix into a standard form



def solution(states):
    if not check_if_square(deepcopy(states)):
        return None

    states_original = deepcopy(states)
    states = populate_absorbing_states(states)
    lcm = get_lcm(states)
    states = make_all_states_equal(states, lcm)
    standard_form(states, lcm, states_original)


    pass
        


lst = [
    [5, 2, 0],
    [0, 0, 0],
    [2, 0, 0]
]

solution(lst)


# pprint(transform_to_tuples(deepcopy(lst)))

# lst = populate_absorbing_states(lst)

# arr = np.empty((len(lst), len(lst)), dtype=np.int)
# arr[:] = lst
# pprint(arr)

# pprint(np.linalg.inv(arr))
# https://youtu.be/qhnFHnLkrfA?t=802




