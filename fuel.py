# Markhov chains - https://www.youtube.com/watch?v=bTeKu7WdbT8
# For example, consider the matrix m:
# [
#   [0,1,0,0,0,1],  
#   [4,0,0,3,2,0],  
#   [0,0,0,0,0,0],  
#   [0,0,0,0,0,0],  
#   [0,0,0,0,0,0],  
#   [0,0,0,0,0,0],  
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
# solution.solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
# Output:
#     [7, 6, 8, 21]

# Input:
# solution.solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
# Output:
#     [0, 3, 2, 9, 14]

import numpy as np
from fractions import gcd, Fraction
from functools import reduce
from copy import deepcopy
from pprint import pprint


def transform_to_fractions(states):
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
                    states[x][y] = Fraction(1, 1)
                else:
                    states[x][y] = Fraction(0, 1)
        else:
            for y in range(len(states[x])):
                states[x][y] = Fraction(states[x][y], sum)
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
    
    changes = [-1 for x in range(len(states))]
    absorbing_states = []
    nonabsorbing_states = []

    for x in range(len(states)):
        if absorbing_states_indexes[x]:
            absorbing_states.append(states[x])
        else:
            nonabsorbing_states.append(states[x])
    
    amount = 0
    for value in absorbing_states_indexes:
        if value:
            amount += 1
    current_amount = amount

    standard_form = [[0 for _ in range(len(states))] for _ in range(len(states))]
    for x in range(len(absorbing_states)):
        state = absorbing_states[x]
        for y in range(len(state)):
            if state[y] == lcm:
                changes[y] = amount - current_amount
                current_amount -= 1
                break

    missing = [x for x in range(len(states))]
    for value in changes:
        if not value == -1:
            missing.remove(value)

    for x in range(len(changes)):
        if changes[x] == -1:
            changes[x] = missing.pop()

    for (x, x_changed) in zip(range(len(changes)), changes):
        for (y, y_changed) in zip(range(len(changes)), changes):
            standard_form[x_changed][y_changed] = states[x][y]

    return (standard_form, amount, changes)

def zeros_matrix(rows, cols):
    A = []
    for i in range(rows):
        A.append([])
        for j in range(cols):
            A[-1].append(0.0)

    return A

def copy_matrix(M):
    rows = len(M)
    cols = len(M[0])

    MC = zeros_matrix(rows, cols)

    for i in range(rows):
        for j in range(rows):
            MC[i][j] = M[i][j]

    return MC

def matrix_multiply(A,B):
    rowsA = len(A)
    colsA = len(A[0])

    rowsB = len(B)
    colsB = len(B[0])

    C = zeros_matrix(rowsA, colsB)

    for i in range(rowsA):
        for j in range(colsB):
            total = 0
            for ii in range(colsA):
                total += A[i][ii] * B[ii][j]
            C[i][j] = total

    return C

def invert_matrix(A, I):
    """
    Returns the inverse of the passed in matrix.
        :param A: The matrix to be inversed
 
        :return: The inverse of the matrix A
    """
    # Section 1: Make sure A can be inverted.
 
    # Section 2: Make copies of A & I, AM & IM, to use for row ops
    n = len(A)
    AM = copy_matrix(A)
    IM = copy_matrix(I)
 
    # Section 3: Perform row operations
    indices = list(range(n)) # to allow flexible row referencing ***
    for fd in range(n): # fd stands for focus diagonal
        fdScaler = 1.0 / AM[fd][fd]
        # FIRST: scale fd row with fd inverse. 
        for j in range(n): # Use j to indicate column looping.
            AM[fd][j] *= fdScaler
            IM[fd][j] *= fdScaler
        # SECOND: operate on all rows except fd row as follows:
        for i in indices[0:fd] + indices[fd+1:]: 
            # *** skip row with fd in it.
            crScaler = AM[i][fd] # cr stands for "current row".
            for j in range(n): 
                # cr - crScaler * fdRow, but one element at a time.
                AM[i][j] = AM[i][j] - crScaler * AM[fd][j]
                IM[i][j] = IM[i][j] - crScaler * IM[fd][j]
    return IM

def print_list(lst):
    for line in lst:
        print line

def solution(states):
    if not check_if_square(deepcopy(states)):
        return None

    states_original = deepcopy(states)
    states = populate_absorbing_states(states)
    states = transform_to_fractions(states)
    print_list(states)
    lcm = Fraction(1, 1)

    states, amount, changes = standard_form(states, lcm, states_original)
    print_list(states)

    dim_size = len(states) - amount
    dim = (dim_size, dim_size)

    Q_matrix = np.empty(dim, dtype=Fraction)
    Q_matrix[:] = [state[amount:] for state in states[amount:]]
    print "Q_matrix\n", Q_matrix

    I_matrix = np.identity(dim_size, dtype=Fraction)
    # for x in range(len(I_matrix)):
    #     for y in range(len(I_matrix[x])):
    #         if I_matrix[x][y] == 1:
    #             I_matrix[x][y] = lcm
    print "I_matrix\n", I_matrix
    
    R_matrix = np.zeros((dim_size, amount), dtype=Fraction)
    R_matrix[:] = [state[:amount] for state in states[amount:]]
    print "R_matrix\n", R_matrix

    F_matrix_inv = I_matrix - Q_matrix
    print "F_matrix_inv\n", F_matrix_inv

    # F_matrix = np.zeros(dim)
    # F_matrix[:] = invert_matrix(F_matrix_inv, I_matrix)

    # FR_matrix = matrix_multiply(list(F_matrix), list(R_matrix))

    # I_matrix = np.identity(amount)
    # # for x in range(len(I_matrix)):
    # #     for y in range(len(I_matrix[x])):
    # #         if I_matrix[x][y] == 1:
    # #             I_matrix[x][y] = lcm
    # I_matrix = list(I_matrix)
    
    # limiting_matrix = [[0 for _ in range(len(states))] for _ in range(len(states))]

    # for x in range(len(I_matrix)):
    #     for y in range(len(I_matrix[x])):
    #         limiting_matrix[x][y] = I_matrix[x][y]
    
    # for x in range(len(FR_matrix)):
    #     for y in range(len(FR_matrix[x])):
    #         limiting_matrix[x + amount][y] = FR_matrix[x][y]

    # values = [0 for _ in range(amount + 1)]
    # for y in range(amount):
    #     for x in range(amount, len(states)):
    #         values[changes.index(y) - (len(states) - amount)] += limiting_matrix[x][y]
    # values[amount] = lcm
    # return values



lst_0 = [[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

lst_1 = [
  [0,1,0,0,0,1],  
  [4,0,0,3,2,0],  
  [0,0,0,0,0,0],  
  [0,0,0,0,0,0],  
  [0,0,0,0,0,0],  
  [0,0,0,0,0,0],  
]

print solution(lst_1)


# pprint(transform_to_tuples(deepcopy(lst)))

# lst = populate_absorbing_states(lst)

# arr = np.empty((len(lst), len(lst)))
# arr[:] = lst
# pprint(arr)

# pprint(np.linalg.inv(arr))
# https://youtu.be/qhnFHnLkrfA?t=802




