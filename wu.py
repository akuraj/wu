import numpy as np
import time
from state import get_state
from utils import (search_board, search_point, search_point_own,
                   search_board_next_sq, search_point_next_sq, search_point_own_next_sq,
                   get_pattern, apply_pattern, assert_nb, set_sq, clear_sq,
                   get_point_on_line)
from numba import njit
from consts import OWN, EMPTY, BLACK, WHITE, NOT_OWN, WALL, STONE
from pattern import P_3_B, P_4_ST, P_4_A, PATTERNS
from functools import reduce


state = get_state(["a1", "a2", "a3", "a13", "a14", "a15", "b1", "b15", "c1", "c15",
                   "f14", "g13", "i9", "i10", "m1", "m15", "n1", "n15", "o1", "o2",
                   "o3", "o13", "o14", "o15"],
                  ["i6", "i13", "j10"],
                  BLACK,
                  False)

print(state)


def is_win(board, color, point):
    set_sq(board, color, point)

    threats = []
    csqss = []
    for p in PATTERNS:
        p_threats = search_point_own(board, p.pattern, color, point, p.own_sqs)
        p_csqss = [set([get_point_on_line(x[0], x[1], y) for y in p.critical_sqs])
                   for x in p_threats]
        threats.extend(p_threats)
        csqss.extend(p_csqss)

    csqs = reduce(set.intersection, csqss)

    won = len(threats) > 0 and len(csqs) == 0

    if not won:
        for csq in csqs:
            set_sq(board, color ^ STONE, csq)

        threats_next_sq = []
        for p in PATTERNS:
            threats_next_sq.extend(search_point_own_next_sq(board, p.pattern,
                                                            color, point, p.own_sqs))

        next_sqs = [x[0] for x in threats_next_sq]
        for next_sq in next_sqs:
            if is_win(board, color, next_sq):
                won = True
                break

        for csq in csqs:
            clear_sq(board, color ^ STONE, csq)

    clear_sq(board, color, point)

    return won


print(is_win(state.board, BLACK, (1, 5)))


# black_threats = [search_board(state.board, p.pattern, BLACK) for p in PATTERNS]
# black_threats_next_sq = [search_board_next_sq(state.board, p.pattern, BLACK) for p in PATTERNS]
# print(black_threats_next_sq)


# start = time.monotonic()

# end = time.monotonic()
# print("Time taken: ", end - start, " seconds")
