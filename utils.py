from numba import njit
from consts import NUM_DIRECTIONS


@njit
def is_symmetric(pattern):
    """Check symmetry of 1d pattern."""

    assert pattern.ndim == 1
    n = pattern.size
    for i in range(int(n / 2)):
        if pattern[i] != pattern[n - i - 1]:
            return False
    else:
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
def pattern_search(board, pattern, color):
    """Search for a 1d pattern on a 2d board."""

    assert board.ndim == 2
    assert pattern.ndim == 1
    assert board.shape[0] == board.shape[1]
    side = board.shape[0]
    length = pattern.size

    symmetric = is_symmetric(pattern)
    ndirs = int(NUM_DIRECTIONS / 2) if symmetric else NUM_DIRECTIONS

    # TODO: Use numpy array instead of list for "found".
    found = []
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
                    found.append(((i, j), direction))

    return found
