import numpy as np
from numba import njit
from consts import (SIDE_LEN, SIDE_LEN_ACT, NUM_DIRECTIONS, WALL, BLACK, WHITE,
                    EMPTY, STONE)


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
    if color == BLACK:
        return gen_pattern
    elif color == WHITE:
        pattern = np.full(gen_pattern.size, EMPTY, dtype=np.byte)

        for i, val in enumerate(gen_pattern):
            # Switch the BLACK and WHITE bits.
            pattern[i] = val if val & STONE in (STONE, 0) else val ^ STONE

        return pattern
    else:
        raise Exception("Invalid color!")


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
def increments(d):
    return (increment_fn(d), increment_fn(d + 2))


@njit
def index_bounds(side, length, increment):
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
def index_bounds_incl(side, length, x, y, row_inc, col_inc):
    row_b = side
    row_f = side
    if row_inc == -1:
        row_f = x + 1
        row_b = side - row_f
    elif row_inc == 0:
        pass
    elif row_inc == 1:
        row_b = x
        row_f = side - row_b
    else:
        raise Exception("Invalid row_inc!")

    col_b = side
    col_f = side
    if col_inc == -1:
        col_f = y + 1
        col_b = side - col_f
    elif col_inc == 0:
        pass
    elif col_inc == 1:
        col_b = y
        col_f = side - col_b
    else:
        raise Exception("Invalid col_inc!")

    back = min(row_b, col_b)
    front = min(row_f, col_f)

    return(-min(back, length - 1), min(front, length) - (length - 1))


@njit
def dedupe_matches(matches):
    i = 0
    n = len(matches)

    while i < n - 1:
        val = matches[i]
        j = i + 1

        while j < n:
            if matches[j] == val or matches[j] == val[::-1]:
                del matches[j]
                n -= 1
            else:
                j += 1

        i += 1


@njit
def search_board(board, gen_pattern, color):
    """Search for a 1d pattern on a 2d board."""

    side = board.shape[0]
    pattern = get_pattern(gen_pattern, color)
    length = pattern.size

    symmetric = is_symmetric(pattern)
    ndirs = int(NUM_DIRECTIONS / 2) if symmetric else NUM_DIRECTIONS

    matches = []
    for d in range(ndirs):
        (row_inc, col_inc) = increments(d)
        (row_min, row_max) = index_bounds(side, length, row_inc)
        (col_min, col_max) = index_bounds(side, length, col_inc)

        for i in range(row_min, row_max):
            for j in range(col_min, col_max):
                for k in range(length):
                    if not pattern[k] & board[i + row_inc * k, j + col_inc * k]:
                        break
                else:
                    # Store Ordered Line Segment, a -> b, where the pattern lies.
                    a = (i, j)
                    b = (i + row_inc * (length - 1), j + col_inc * (length - 1))
                    matches.append((a, b))

    dedupe_matches(matches)
    return matches


@njit
def search_point(board, gen_pattern, color, point):
    """Search for a 1d pattern on a 2d board including the given point."""

    (x, y) = point

    side = board.shape[0]
    pattern = get_pattern(gen_pattern, color)
    length = pattern.size

    symmetric = is_symmetric(pattern)
    ndirs = int(NUM_DIRECTIONS / 2) if symmetric else NUM_DIRECTIONS

    matches = []
    for d in range(ndirs):
        (row_inc, col_inc) = increments(d)
        (s_min, s_max) = index_bounds_incl(side, length, x, y, row_inc, col_inc)

        for h in range(s_min, s_max):
            (i, j) = (x + row_inc * h, y + col_inc * h)

            for k in range(length):
                if not pattern[k] & board[i + row_inc * k, j + col_inc * k]:
                    break
            else:
                # Store Ordered Line Segment, a -> b, where the pattern lies.
                a = (i, j)
                b = (i + row_inc * (length - 1), j + col_inc * (length - 1))
                matches.append((a, b))

    dedupe_matches(matches)
    return matches


@njit
def search_point_own(board, gen_pattern, color, point, own_sqs):
    """Search for a 1d pattern on a 2d board including the given point as an own_sq."""

    (x, y) = point

    side = board.shape[0]
    pattern = get_pattern(gen_pattern, color)
    length = pattern.size

    symmetric = is_symmetric(pattern)
    ndirs = int(NUM_DIRECTIONS / 2) if symmetric else NUM_DIRECTIONS

    matches = []

    # We are searching for patterns including the given point as an "own_sq".
    if board[point] == color:
        for d in range(ndirs):
            (row_inc, col_inc) = increments(d)
            (s_min, s_max) = index_bounds_incl(side, length, x, y, row_inc, col_inc)

            for own_sq in own_sqs:
                if s_min <= -own_sq < s_max:
                    (i, j) = (x - row_inc * own_sq, y - col_inc * own_sq)

                    for k in range(length):
                        if not pattern[k] & board[i + row_inc * k, j + col_inc * k]:
                            break
                    else:
                        # Store Ordered Line Segment, a -> b, where the pattern lies.
                        a = (i, j)
                        b = (i + row_inc * (length - 1), j + col_inc * (length - 1))
                        matches.append((a, b))

    dedupe_matches(matches)
    return matches


@njit
def dedupe_next_sq_match_pairs(pairs):
    i = 0
    n = len(pairs)

    while i < n - 1:
        a = pairs[i]
        j = i + 1

        while j < n:
            b = pairs[j]
            if a[0] == b[0] and (a[1] == b[1] or a[1] == b[1][::-1]):
                del pairs[j]
                n -= 1
            else:
                j += 1

        i += 1


@njit
def search_board_next_sq(board, gen_pattern, color):
    """Search for a 1d pattern on a 2d board.

    Returns "next_sq"s and the corresponding pattern matches (as in above functions)
    as a list of (next_sq, match) pairs.

    In existing terminology, "point" is a "rest" square,
    and "next_sq" is the "gain" square.
    """

    side = board.shape[0]
    pattern = get_pattern(gen_pattern, color)
    length = pattern.size

    symmetric = is_symmetric(pattern)
    ndirs = int(NUM_DIRECTIONS / 2) if symmetric else NUM_DIRECTIONS

    next_sq_match_pairs = []
    for d in range(ndirs):
        (row_inc, col_inc) = increments(d)
        (row_min, row_max) = index_bounds(side, length, row_inc)
        (col_min, col_max) = index_bounds(side, length, col_inc)

        for i in range(row_min, row_max):
            for j in range(col_min, col_max):
                found_next_sq = False
                k_next_sq = -1

                for k in range(length):
                    p_val = pattern[k]
                    b_val = board[i + row_inc * k, j + col_inc * k]

                    if not p_val & b_val:
                        if not found_next_sq and p_val == color and b_val == EMPTY:
                            found_next_sq = True
                            k_next_sq = k
                        else:
                            break
                else:
                    if found_next_sq:
                        # Store Ordered Line Segment, a -> b, where the pattern lies.
                        a = (i, j)
                        b = (i + row_inc * (length - 1), j + col_inc * (length - 1))
                        next_sq = (i + row_inc * k_next_sq, j + col_inc * k_next_sq)
                        next_sq_match_pairs.append((next_sq, (a, b)))

    dedupe_next_sq_match_pairs(next_sq_match_pairs)
    return next_sq_match_pairs


@njit
def search_point_next_sq(board, gen_pattern, color, point):
    """Search for a 1d pattern on a 2d board including the given point.

    Returns "next_sq"s and the corresponding pattern matches (as in above functions)
    as a list of (next_sq, match) pairs.

    In existing terminology, "point" is a "rest" square,
    and "next_sq" is the "gain" square.
    """

    (x, y) = point

    side = board.shape[0]
    pattern = get_pattern(gen_pattern, color)
    length = pattern.size

    symmetric = is_symmetric(pattern)
    ndirs = int(NUM_DIRECTIONS / 2) if symmetric else NUM_DIRECTIONS

    next_sq_match_pairs = []
    for d in range(ndirs):
        (row_inc, col_inc) = increments(d)
        (s_min, s_max) = index_bounds_incl(side, length, x, y, row_inc, col_inc)

        for h in range(s_min, s_max):
            (i, j) = (x + row_inc * h, y + col_inc * h)

            found_next_sq = False
            k_next_sq = -1

            for k in range(length):
                p_val = pattern[k]
                b_val = board[i + row_inc * k, j + col_inc * k]

                if not p_val & b_val:
                    if not found_next_sq and p_val == color and b_val == EMPTY:
                        found_next_sq = True
                        k_next_sq = k
                    else:
                        break
            else:
                if found_next_sq:
                    # Store Ordered Line Segment, a -> b, where the pattern lies.
                    a = (i, j)
                    b = (i + row_inc * (length - 1), j + col_inc * (length - 1))
                    next_sq = (i + row_inc * k_next_sq, j + col_inc * k_next_sq)
                    next_sq_match_pairs.append((next_sq, (a, b)))

    dedupe_next_sq_match_pairs(next_sq_match_pairs)
    return next_sq_match_pairs


@njit
def search_point_own_next_sq(board, gen_pattern, color, point, own_sqs):
    """Search for a 1d pattern on a 2d board including the given point as an own_sq.

    Returns "next_sq"s and the corresponding pattern matches (as in above functions)
    as a list of (next_sq, match) pairs.

    In existing terminology, "point" is a "rest" square,
    and "next_sq" is the "gain" square.
    """

    (x, y) = point

    side = board.shape[0]
    pattern = get_pattern(gen_pattern, color)
    length = pattern.size

    symmetric = is_symmetric(pattern)
    ndirs = int(NUM_DIRECTIONS / 2) if symmetric else NUM_DIRECTIONS

    next_sq_match_pairs = []

    # We are searching for patterns including the given point as an "own_sq".
    if board[point] == color:
        for d in range(ndirs):
            (row_inc, col_inc) = increments(d)
            (s_min, s_max) = index_bounds_incl(side, length, x, y, row_inc, col_inc)

            for own_sq in own_sqs:
                if s_min <= -own_sq < s_max:
                    (i, j) = (x - row_inc * own_sq, y - col_inc * own_sq)

                    found_next_sq = False
                    k_next_sq = -1

                    for k in range(length):
                        p_val = pattern[k]
                        b_val = board[i + row_inc * k, j + col_inc * k]

                        if not p_val & b_val:
                            if not found_next_sq and p_val == color and b_val == EMPTY:
                                found_next_sq = True
                                k_next_sq = k
                            else:
                                break
                    else:
                        if found_next_sq:
                            # Store Ordered Line Segment, a -> b, where the pattern lies.
                            a = (i, j)
                            b = (i + row_inc * (length - 1), j + col_inc * (length - 1))
                            next_sq = (i + row_inc * k_next_sq, j + col_inc * k_next_sq)
                            next_sq_match_pairs.append((next_sq, (a, b)))

    dedupe_next_sq_match_pairs(next_sq_match_pairs)
    return next_sq_match_pairs


def row_idx_to_num(x):
    assert 1 <= x <= SIDE_LEN_ACT
    return(SIDE_LEN_ACT + 1 - x)


row_num_to_idx = row_idx_to_num


def col_idx_to_chr(x):
    assert 1 <= x <= SIDE_LEN_ACT
    return(chr(ord("a") + x - 1))


def col_chr_to_idx(x):
    idx = ord(x) - ord("a") + 1
    assert 1 <= idx <= SIDE_LEN_ACT
    return idx


def point_to_algebraic(x):
    assert len(x) == 2
    row_num = row_idx_to_num(x[0])
    col_chr = col_idx_to_chr(x[1])
    return f"{col_chr}{row_num}"


def algebraic_to_point(x):
    col_idx = col_chr_to_idx(x[0])
    row_idx = row_num_to_idx(int(x[1:]))
    return(row_idx, col_idx)


@njit
def apply_pattern(board, pattern, point, d):
    """Apply given pattern at given point in given direction.

    Returns True if application was succesful.
    Else, returns False.
    If application fails then board is unchanged.

    We only check that the length fits at that point.
    We will apply a non-standard element as it is,
    including overwriting a wall with any element whatsoever.

    Useful for testing purposes.
    """

    (x, y) = point

    side = board.shape[0]
    length = pattern.size

    (row_inc, col_inc) = increments(d)

    can_apply = True
    for k in range(length):
        (i, j) = (x + row_inc * k, y + col_inc * k)
        if i not in range(side) or j not in range(side):
            can_apply = False
            break

    if can_apply:
        for k in range(length):
            # NOTE: If it's a non-standard element, we just apply it as is.
            board[x + row_inc * k, y + col_inc * k] = pattern[k]

    return can_apply
