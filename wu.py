import numpy as np
import time
from state import get_state
from utils import (search_board, search_point, search_point_own,
                   search_board_next_sq, search_point_next_sq, search_point_own_next_sq,
                   get_pattern, apply_pattern, assert_nb, set_sq, clear_sq,
                   point_on_line, point_set_on_line, new_search_node,
                   next_sqs_from_node, lines_from_next_sqs_arr,
                   chebyshev_distance)
from numba import njit
from consts import OWN, EMPTY, BLACK, WHITE, NOT_OWN, WALL, STONE, MAX_DEFCON
from pattern import (P_3_B, P_4_ST, P_4_A, PATTERNS,
                     search_all_board, search_all_point, search_all_point_own,
                     search_all_board_next_sq, search_all_point_next_sq,
                     search_all_point_own_next_sq)
from functools import reduce


# state = get_state(["a1", "a2", "a3", "a13", "a14", "a15", "b1", "b15", "c1", "c15",
#                    "f14", "g13", "i9", "i10", "m1", "m15", "n1", "n15", "o1", "o2",
#                    "o3", "o13", "o14", "o15"],
#                   ["i6", "i13", "j10"],
#                   BLACK,
#                   False)

state = get_state(["f5", "g5", "h5", "g6", "g7", "h7", "i7", "h8", "h9", "g9", "i9"],
                  ["g4", "e5", "f6", "h6", "j6", "f7", "j7", "f8", "g8", "i8", "f9"],
                  BLACK,
                  True)

print(state)


def threat_space_search(board, color, point=None):
    if point:
        set_sq(board, color, point)

    threats = (search_all_point_own(board, color, point)
               if point
               else search_all_board(board, color))
    csqs = reduce(set.intersection, [x["critical_sqs"] for x in threats]) if threats else set()
    potential_win = len(threats) > 0 and len(csqs) == 0
    children = []

    if not potential_win:
        for csq in csqs:
            set_sq(board, color ^ STONE, csq)

        # TODO: Can we fix duplication of effort?
        threats_next_sq = (search_all_point_own_next_sq(board, color, point)
                           if point
                           else search_all_board_next_sq(board, color))
        next_sqs = set([x["next_sq"] for x in threats_next_sq])

        children = [threat_space_search(board, color, x) for x in next_sqs]
        potential_win = any([x["potential_win"] for x in children])

        if not point and not potential_win and len(children) > 1:
            next_sqs_children = [next_sqs_from_node(x) for x in children]
            lines_dict = lines_from_next_sqs_arr(next_sqs_children)

            for line_set in lines_dict.values():
                line = list(line_set)
                num_pts = len(line)
                for i in range(num_pts):
                    for j in range(i + 1, num_pts):
                        idx_i = line[i][1]
                        idx_j = line[j][1]
                        p_i = line[i][0]
                        p_j = line[j][0]
                        if (idx_i != idx_j and
                            chebyshev_distance(p_i, p_j) < MAX_DEFCON):
                            node_i = children[line[i][1]]
                            node_j = children[line[j][1]]

                            # WORKING HERE.



        for csq in csqs:
            clear_sq(board, color ^ STONE, csq)

    if point:
        clear_sq(board, color, point)

    return new_search_node(point, threats, csqs, potential_win, children)


# n = 10000

# for _ in range(n):
#     threat_space_search(state.board, state.turn)

# start = time.monotonic()
# for _ in range(n):
#     threat_space_search(state.board, state.turn)
# end = time.monotonic()
# print("Time taken: ", end - start, " seconds")

node = threat_space_search(state.board, state.turn)
for child in node["children"]:
    if child["potential_win"]:
        print(child["next_sq"])
