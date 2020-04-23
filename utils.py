from numba import njit
from consts import NUM_DIRECTIONS, OWN, OPP, EMPTY
import numpy as np


@njit
def get_side(board):
    assert board.ndim == 2
    assert board.shape[0] == board.shape[1]
    return board.shape[0]


@njit
def get_pattern_info(gen_pattern, color, opp_end_is_closed):
    assert gen_pattern.ndim == 1
    gen_length = gen_pattern.size

    is_closed_end = False
    if opp_end_is_closed:
        for i in range(gen_length):
            if gen_pattern[i] in (OWN, EMPTY):
                pass
            elif gen_pattern[i] == OPP:
                # Not allowed to be closed at the beginning of the pattern.
                assert i != 0

                # If closed at the end, we need to handle it.
                is_closed_end = (i == gen_length - 1)
            else:
                raise Exception("Invalid element in gen_pattern!")

    length = gen_length if not is_closed_end else gen_length - 1
    pattern = np.full(length, EMPTY, dtype=np.byte)
    for i in range(length):
        pattern[i] = gen_pattern[i] * color

    return (pattern, is_closed_end)


@njit
def is_symmetric(pattern):
    """Check symmetry of 1d pattern."""

    n = pattern.size
    for i in range(int(n / 2)):
        if pattern[i] != pattern[n - i - 1]:
            return False

    return True


@njit
def increment_fn(i):
    if i % 4 == 0:
        return 0
    elif i % 8 < 4:
        return 1
    else:
        return -1


@njit
def increments(direction):
    return (increment_fn(direction), increment_fn(direction + 2))


@njit
def index_bounds(side, length, increment):
    assert length > 0

    if length <= side:
        if increment == 0:
            return (0, side)
        elif increment == 1:
            return (0, side - length + 1)
        elif increment == -1:
            return (length - 1, side)
        else:
            raise Exception("Invalid increment!")
    else:
        return (0, 0)


@njit
def pattern_search(board, gen_pattern, color, opp_end_is_closed):
    """Search for a 1d pattern on a 2d board."""

    side = get_side(board)
    (pattern, is_closed_end) = get_pattern_info(gen_pattern, color, opp_end_is_closed)
    length = pattern.size

    symmetric = is_symmetric(pattern)
    ndirs = int(NUM_DIRECTIONS / 2) if symmetric else NUM_DIRECTIONS

    matches = []
    for direction in range(ndirs):
        (row_inc, col_inc) = increments(direction)
        (row_min, row_max) = index_bounds(side, length, row_inc)
        (col_min, col_max) = index_bounds(side, length, col_inc)

        for i in range(row_min, row_max):
            for j in range(col_min, col_max):
                for k in range(length):
                    if pattern[k] != board[i + row_inc * k, j + col_inc * k]:
                        break
                else:
                    match = True
                    if is_closed_end:
                        row_end = i + row_inc * length
                        col_end = j + col_inc * length

                        if 0 <= row_end < side and 0 <= col_end < side:
                            match = (board[row_end, col_end] == -color)

                    if match:
                        matches.append(((i, j), direction))

    return matches
