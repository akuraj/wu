import numpy as np
from numba import njit
from consts import SIDE_LEN, NUM_DIRECTIONS, WALL, BLACK, WHITE, EMPTY, STONE

# TODO: Fix the way we compute increments?
# TODO: Should we keep returning pattern matches as a set?


@njit
def new_board():
    board = np.full((SIDE_LEN, SIDE_LEN), EMPTY, dtype=np.byte)

    # Set the walls.
    for wall in (0, SIDE_LEN - 1):
        for i in range(SIDE_LEN):
            board[wall, i] = WALL
            board[i, wall] = WALL

    return board


@njit
def get_pattern(gen_pattern, color):
    assert gen_pattern.ndim == 1

    if color == BLACK:
        return gen_pattern
    elif color == WHITE:
        pattern = np.full(gen_pattern.size, EMPTY, dtype=np.byte)

        for i, val in enumerate(gen_pattern):
            # Switch the BLACK and WHITE bits.
            pattern[i] = val if val & STONE == STONE else val ^ STONE

        return pattern
    else:
        raise Exception("Invalid color!")


@njit
def get_side(board):
    assert board.ndim == 2
    assert board.shape[0] == board.shape[1]
    return board.shape[0]


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
def pattern_search(board, gen_pattern, color):
    """Search for a 1d pattern on a 2d board."""

    side = get_side(board)
    pattern = get_pattern(gen_pattern, color)
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
                    if not pattern[k] & board[i + row_inc * k, j + col_inc * k]:
                        break
                else:
                    # Store Ordered Line Segment where the pattern lies.
                    a = (i, j)
                    b = (i + row_inc * (length - 1), j + col_inc * (length - 1))
                    matches.append((a, b) if a < b else (b, a))

    return set(matches)
