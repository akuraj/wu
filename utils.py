from enum import IntEnum, auto, unique
import numpy as np
from numba import njit
from consts import (SIDE_LEN, SIDE_LEN_ACT, NUM_DIRECTIONS, WALL, BLACK, WHITE,
                    EMPTY, STONE, COLORS, WIN_LENGTH, OWN, MAX_DEFCON)
from geometry import (increments, index_bounds, index_bounds_incl,
                      is_normal_line, chebyshev_distance, slope_intercept,
                      point_idx_on_line)


@njit
def assert_nb(truth_value, assert_err_msg=""):
    if not truth_value:
        print(assert_err_msg)
        raise Exception


@njit
def new_board():
    board = np.full((SIDE_LEN, SIDE_LEN), EMPTY, dtype=np.byte)

    # Set the walls.
    for wall in (0, SIDE_LEN - 1):
        for i in range(SIDE_LEN):
            board[wall, i] = WALL
            board[i, wall] = WALL

    return board


def get_board(blacks, whites):
    assert not set.intersection(set(blacks), set(whites))

    board = new_board()

    for elem in blacks:
        board[algebraic_to_point(elem)] = BLACK

    for elem in whites:
        board[algebraic_to_point(elem)] = WHITE

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

    matches = []
    for d in range(NUM_DIRECTIONS):
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

    matches = []
    for d in range(NUM_DIRECTIONS):
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

    matches = []

    # We are searching for patterns including the given point as an "own_sq".
    if board[point] == color:
        for d in range(NUM_DIRECTIONS):
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

    next_sq_match_pairs = []
    for d in range(NUM_DIRECTIONS):
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

    next_sq_match_pairs = []
    for d in range(NUM_DIRECTIONS):
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

    next_sq_match_pairs = []

    # We are searching for patterns including the given point as an "own_sq".
    if board[point] == color:
        for d in range(NUM_DIRECTIONS):
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
    return SIDE_LEN_ACT + 1 - x


row_num_to_idx = row_idx_to_num


def col_idx_to_chr(x):
    assert 1 <= x <= SIDE_LEN_ACT
    return chr(ord("a") + x - 1)


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
    return (row_idx, col_idx)


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


@njit
def matches_are_subset(x, y):
    for a in x:
        found = False
        for b in y:
            if a == b or a == b[::-1]:
                found = True
                break

        if not found:
            return False

    return True


@njit
def matches_are_equal(x, y):
    # pylint: disable=W1114
    return matches_are_subset(x, y) and matches_are_subset(y, x)


@njit
def next_sq_matches_are_subset(x, y):
    for a in x:
        found = False
        for b in y:
            if a[0] == b[0] and (a[1] == b[1] or a[1] == b[1][::-1]):
                found = True
                break

        if not found:
            return False

    return True


@njit
def next_sq_matches_are_equal(x, y):
    # pylint: disable=W1114
    return next_sq_matches_are_subset(x, y) and next_sq_matches_are_subset(y, x)


@njit
def set_sq(board, color, point):
    assert color in COLORS
    assert board[point] == EMPTY
    board[point] = color


@njit
def clear_sq(board, color, point):
    assert color in COLORS
    assert board[point] == color
    board[point] = EMPTY


def set_sqs(board, color, sqs):
    if sqs is not None:
        for sq in sqs:
            set_sq(board, color, sq)


def clear_sqs(board, color, sqs):
    if sqs is not None:
        for sq in sqs:
            clear_sq(board, color, sq)


@njit
def degree(gen_pattern):
    """Maximum number of 'OWN's in a sub-sequence of length = WIN_LENGTH,
    full of OWN/EMPTY sqs."""

    n = len(gen_pattern)
    max_owns = 0
    for i in range(n - WIN_LENGTH + 1):
        owns = 0
        for j in range(WIN_LENGTH):
            if gen_pattern[i + j] not in (OWN, EMPTY):
                break

            if gen_pattern[i + j] == OWN:
                owns += 1
        else:
            max_owns = max(max_owns, owns)

    return max_owns


@njit
def defcon_from_degree(d):
    return MAX_DEFCON - d


@njit
def is_one_step_from_straight_threat(gen_pattern):
    """True if a straight threat (straight four) can be
    achieved in one move."""

    n = len(gen_pattern)

    # Length of a straight threat: WIN_LENGTH - 1 OWN's in a row,
    # with an empty space on either side.
    l = WIN_LENGTH + 1

    for idx, v in enumerate(gen_pattern):
        if v == EMPTY:
            for i in range(n - l + 1):
                for j in range(l):
                    # Straight threat pattern value.
                    value = EMPTY if j == 0 or j == l - 1 else OWN

                    if i + j == idx:
                        if value != OWN:
                            break
                    else:
                        if value != gen_pattern[i + j]:
                            break
                else:
                    return True

    return False


def new_threat_seq_item(next_sq, critical_sqs=None):
    item = {"next_sq": next_sq,
            "critical_sqs": critical_sqs}

    return item


@unique
class MoveType(IntEnum):
    EMPTY = auto()
    POINT = auto()
    COMBINATION = auto()


def new_move(threat_seqs=[]):
    next_sqs = None
    critical_sqs = None
    last_sqs = []
    move_type = MoveType.EMPTY

    if not threat_seqs:
        pass
    elif len(threat_seqs) == 1:
        assert len(threat_seqs[0]) == 1
        next_sqs = set([threat_seqs[0][0]["next_sq"]])
        critical_sqs = threat_seqs[0][0]["critical_sqs"]
        last_sqs.append(threat_seqs[0][0]["next_sq"])
        move_type = MoveType.POINT
    else:
        next_sqs = set()
        critical_sqs = set()
        for threat_seq in threat_seqs:
            seq_len = len(threat_seq)
            assert seq_len > 0
            for i, item in enumerate(threat_seq):
                assert item["next_sq"] not in next_sqs
                next_sqs.add(item["next_sq"])

                assert not critical_sqs.intersection(item["critical_sqs"])
                critical_sqs.update(item["critical_sqs"])

                if i == seq_len - 1:
                    last_sqs.append(item["next_sq"])

        move_type = MoveType.COMBINATION

    if next_sqs is not None and critical_sqs is not None:
        assert not set.intersection(next_sqs, critical_sqs)

    move = {"threat_seqs": threat_seqs,
            "next_sqs": next_sqs,
            "critical_sqs": critical_sqs,
            "last_sqs": last_sqs,
            "move_type": move_type}

    return move


def new_search_node(move, threats=[], potential_win=False, children=[]):
    node = {"move": move,
            "threats": threats,
            "potential_win": potential_win,
            "children": children}

    return node


def get_threat_sequence(node, path):
    sequence = []

    sub_node = node
    for seq in sub_node["move"]["threat_seqs"]:
        sequence.extend(seq)

    for idx in path:
        sub_node = sub_node["children"][idx]
        for seq in sub_node["move"]["threat_seqs"]:
            sequence.extend(seq)

    return sequence


def next_sqs_info_from_node(node, path=[], cumulative_nsqs=set(),
                            cumulative_csqs=set()):
    next_sqs_info = []

    next_sqs = (node["move"]["next_sqs"]
                if node["move"]["next_sqs"] is not None
                else set())
    critical_sqs = (node["move"]["critical_sqs"]
                    if node["move"]["critical_sqs"] is not None
                    else set())

    cumulative_nsqs_new = set.union(cumulative_nsqs, next_sqs)
    cumulative_csqs_new = set.union(cumulative_csqs, critical_sqs)

    if node["move"]["last_sqs"]:
        next_sqs_info.append({"next_sq": node["move"]["last_sqs"][-1],
                              "path": path.copy(),
                              "cumulative_nsqs": cumulative_nsqs_new,
                              "cumulative_csqs": cumulative_csqs_new})

    for i, child in enumerate(node["children"]):
        next_sqs_info.extend(next_sqs_info_from_node(child,
                                                     path + [i],
                                                     cumulative_nsqs_new,
                                                     cumulative_csqs_new))

    return next_sqs_info


def dedupe_line_items(items):
    i = 0
    n = len(items)

    while i < n - 1:
        val = items[i]
        j = i + 1

        while j < n:
            if items[j][1] == val[1] and items[j][0]["path"] == val[0]["path"]:
                del items[j]
                n -= 1
            else:
                j += 1

        i += 1


def lines_from_next_sqs_info_arr(next_sqs_info_arr):
    next_sqs_info_all = [(y, i) for (i, x) in enumerate(next_sqs_info_arr)
                         for y in x]
    n = len(next_sqs_info_all)

    lines_dict = dict()
    for i in range(n):
        item_i = next_sqs_info_all[i]
        val_i = item_i[0]
        idx_i = item_i[1]
        nsq_i = val_i["next_sq"]
        c_nsqs_i = val_i["cumulative_nsqs"]
        c_csqs_i = val_i["cumulative_csqs"]

        for j in range(i + 1, n):
            item_j = next_sqs_info_all[j]
            val_j = item_j[0]
            idx_j = item_j[1]
            nsq_j = val_j["next_sq"]
            c_nsqs_j = val_j["cumulative_nsqs"]
            c_csqs_j = val_j["cumulative_csqs"]

            # NOTE: Same gain_sq case is being excluded.
            #       It does not need to be handled.
            if (is_normal_line(nsq_i, nsq_j)
                and chebyshev_distance(nsq_i, nsq_j) < MAX_DEFCON
                and idx_i != idx_j
                and not set.intersection(c_nsqs_i, c_csqs_j)
                and not set.intersection(c_csqs_i, c_nsqs_j)
                and not set.intersection(c_csqs_i, c_csqs_j)):

                line = slope_intercept(nsq_i, nsq_j)

                if line in lines_dict:
                    lines_dict[line].append(item_i)
                    lines_dict[line].append(item_j)
                else:
                    lines_dict[line] = [item_i, item_j]

    for v in lines_dict.values():
        dedupe_line_items(v)

    return lines_dict


def point_set_is_useful(point_set, line):
    # Check that the points in the combination are close enough.
    point_idxs = [point_idx_on_line(x[0]["next_sq"], line) for x in point_set]
    point_set_range = max(point_idxs) - min(point_idxs)
    if MAX_DEFCON <= point_set_range:
        return False

    # Check that the point trees are not in conflict.
    n = len(point_set)

    for i in range(n):
        item_i = point_set[i]
        val_i = item_i[0]
        idx_i = item_i[1]
        c_nsqs_i = val_i["cumulative_nsqs"]
        c_csqs_i = val_i["cumulative_csqs"]

        for j in range(i + 1, n):
            item_j = point_set[j]
            val_j = item_j[0]
            idx_j = item_j[1]
            c_nsqs_j = val_j["cumulative_nsqs"]
            c_csqs_j = val_j["cumulative_csqs"]

            if not (idx_i != idx_j
                    and not set.intersection(c_nsqs_i, c_csqs_j)
                    and not set.intersection(c_csqs_i, c_nsqs_j)
                    and not set.intersection(c_csqs_i, c_csqs_j)):
                return False

    return True
