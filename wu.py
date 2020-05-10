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
from collections import deque


state = get_state(["a1", "a2", "a3", "a13", "a14", "a15", "b1", "b15", "c1", "c15",
                   "f14", "g13", "i9", "i10", "m1", "m15", "n1", "n15", "o1", "o2",
                   "o3", "o13", "o14", "o15"],
                  ["i6", "i13", "j10"],
                  BLACK,
                  False)

print(state)


def threat_space_search(board, color, point):
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

    potential_win = len(threats) > 0 and len(csqs) == 0
    variation = deque()  # We will add current point at the end if potential_win.

    if not potential_win:
        for csq in csqs:
            set_sq(board, color ^ STONE, csq)

        threats_next_sq = []
        for p in PATTERNS:
            threats_next_sq.extend(search_point_own_next_sq(board, p.pattern,
                                                            color, point, p.own_sqs))

        next_sqs = [x[0] for x in threats_next_sq]
        for next_sq in next_sqs:
            (potential_win, variation) = threat_space_search(board, color, next_sq)
            if potential_win:
                break

        for csq in csqs:
            clear_sq(board, color ^ STONE, csq)

    clear_sq(board, color, point)

    if potential_win:
        variation.appendleft(point)

    return (potential_win, variation)


# print(threat_space_search(state.board, BLACK, (5, 9)))

threats_next_sq = []
for p in PATTERNS:
    threats_next_sq.extend(search_board_next_sq(state.board, p.pattern, state.turn))

next_sqs = list(set([x[0] for x in threats_next_sq]))

for next_sq in next_sqs:
    print(next_sq, threat_space_search(state.board, state.turn, next_sq))

# start = time.monotonic()

# end = time.monotonic()
# print("Time taken: ", end - start, " seconds")
