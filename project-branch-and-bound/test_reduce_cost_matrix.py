import math
from tsp_solve import MatrixClass


# See additional instructions for these tests in the instructions for the project
def test_reduced_cost_matrix_1():
    input_matrix = [
        [math.inf, 10, 20],
        [15, math.inf, 25],
        [5, 30, math.inf]
    ]
    expected_cost = 40
    expected_matrix = [
        [math.inf, 0, 0],
        [0, math.inf, 0],
        [0, 25, math.inf]
    ]
    state = MatrixClass(input_matrix, 0, [0], {1, 2})
    actual_cost = state.reduce_matrix()
    actual_matrix = state.matrix
    assert actual_cost == expected_cost, f"Expected cost {expected_cost}, but got {actual_cost}"
    for r in range(len(expected_matrix)):
        for c in range(len(expected_matrix[r])):
            assert actual_matrix[r][c] == expected_matrix[r][c], \
                f"Matrix mismatch at [{r}][{c}]: Expected {expected_matrix[r][c]}, got {actual_matrix[r][c]}"


def test_reduced_cost_matrix_2():
    input_matrix = [
        [math.inf, 7, 3, 12],
        [3, math.inf, 6, 14],
        [5, 8, math.inf, 6],
        [9, 3, 5, math.inf]
    ]
    expected_cost = 15
    expected_matrix = [
        [math.inf, 4, 0, 8],
        [0, math.inf, 3, 10],
        [0, 3, math.inf, 0],
        [6, 0, 2, math.inf]
    ]
    state = MatrixClass(input_matrix, 0, [0], {1, 2, 3})
    actual_cost = state.reduce_matrix()
    actual_matrix = state.matrix
    assert actual_cost == expected_cost, f"Expected cost {expected_cost}, but got {actual_cost}"
    for r in range(len(expected_matrix)):
        for c in range(len(expected_matrix[r])):
            assert actual_matrix[r][c] == expected_matrix[r][c], \
                f"Matrix mismatch at [{r}][{c}]"

    # Add more tests as necessary...
