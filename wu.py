import time
from state import get_state
from utils import (new_search_node, next_sqs_info_from_node,
                   lines_from_next_sqs_info_arr, point_set_is_useful,
                   new_move, MoveType, new_threat_seq_item, get_threat_sequence)
from board import set_sqs, clear_sqs
from numba import njit
from consts import BLACK, STONE
from pattern import (ThreatPri, search_all_board, search_all_point_own,
                     search_all_board_get_next_sqs,
                     search_all_point_own_get_next_sqs,
                     search_all_points_own)
from functools import reduce
from itertools import chain, combinations


# state = get_state(["a1", "a2", "a3", "a13", "a14", "a15", "b1", "b15", "c1", "c15",
#                    "f14", "g13", "i9", "i10", "m1", "m15", "n1", "n15", "o1", "o2",
#                    "o3", "o13", "o14", "o15"],
#                   ["i6", "i13", "j10"],
#                   BLACK,
#                   False)

# state = get_state(["f5", "g5", "h5", "g6", "g7", "h7", "i7", "h8", "h9", "g9", "i9"],
#                   ["g4", "e5", "f6", "h6", "j6", "f7", "j7", "f8", "g8", "i8", "f9"],
#                   BLACK,
#                   True)

# state = get_state(["g10", "h8", "i7", "j7", "j9"],
#                   ["g7", "g8", "g9", "i9", "k8"],
#                   BLACK,
#                   True)

state = get_state(["f6", "h6", "g7", "h7", "h8", "g11"],
                  ["e5", "h5", "g6", "l6", "f7", "g8"],
                  BLACK,
                  True)

print(state)


def subsets(s, min_size=0):
    return chain.from_iterable(combinations(s, r) for r in range(min_size, len(s) + 1))


def threat_space_search(board, color, move=new_move(), search_combinations=False):
    # If True, we've been given a specific move to try out,
    # as opposed to being given a starting point to explore from.
    try_move = move["next_sqs"] is not None and move["critical_sqs"] is None

    set_sqs(board, color, move["next_sqs"])

    if not try_move:
        set_sqs(board, color ^ STONE, move["critical_sqs"])

    threats = []
    potential_win = False
    children = []

    if move["move_type"] == MoveType.NONE:
        threats = search_all_board(board, color, ThreatPri.IMMEDIATE)
    elif move["move_type"] == MoveType.POINT:
        threats = search_all_point_own(board, color, move["last_sqs"][0], ThreatPri.IMMEDIATE)
    elif move["move_type"] == MoveType.COMBINATION:
        # TODO: Refine methodology.
        threats = search_all_points_own(board, color, move["last_sqs"], ThreatPri.IMMEDIATE)
    else:
        raise Exception("Invalid move type!")

    # Check if we have a potential win.
    if try_move:
        # Update critical_sqs data in move.
        critical_sqs = (reduce(set.intersection,
                               [x["critical_sqs"] for x in threats])
                        if threats
                        else set())

        # Currently, we can only propose a single point as a move to try out.
        assert move["move_type"] == MoveType.POINT
        move["threat_seqs"][0][0]["critical_sqs"] = critical_sqs
        move["critical_sqs"] = critical_sqs

        potential_win = len(threats) > 0 and len(critical_sqs) == 0
    else:
        potential_win = len(threats) > 0

    # If the move given to try produces no threats, then we stop.
    explore = not try_move or len(threats) > 0

    if explore and not potential_win:
        if try_move:
            set_sqs(board, color ^ STONE, move["critical_sqs"])

        # TODO: Remove duplication of effort.
        # TODO: Remove unnecessary work.
        next_sqs = set()
        if move["move_type"] == MoveType.NONE:
            next_sqs = search_all_board_get_next_sqs(board, color, ThreatPri.ALL)
        elif move["move_type"] == MoveType.POINT:
            next_sqs = search_all_point_own_get_next_sqs(board,
                                                         color,
                                                         move["last_sqs"][0],
                                                         ThreatPri.ALL)
        elif move["move_type"] == MoveType.COMBINATION:
            # TODO: Refine methodology.
            next_sqs_for_combination = [search_all_point_own_get_next_sqs(board,
                                                                          color,
                                                                          x,
                                                                          ThreatPri.ALL)
                                        for x in move["last_sqs"]]
            next_sqs = reduce(set.union, next_sqs_for_combination)
        else:
            raise Exception("Invalid move type!")

        children = [threat_space_search(board,
                                        color,
                                        new_move([[new_threat_seq_item(x)]]))
                    for x in next_sqs]
        potential_win = any([x["potential_win"] for x in children])

        if search_combinations and not potential_win and len(children) > 1:
            next_sqs_info_children = [next_sqs_info_from_node(x) for x in children]
            lines_dict = lines_from_next_sqs_info_arr(next_sqs_info_children)

            children_combinations = []

            for line, info in lines_dict.items():
                point_sets = list(subsets(info, 2))
                for point_set in point_sets:
                    if point_set_is_useful(point_set, line):
                        threat_seqs = [get_threat_sequence(children[x[1]],
                                                           x[0]["path"])
                                       for x in point_set]
                        children_combinations.append(threat_space_search(board,
                                                                         color,
                                                                         new_move(threat_seqs)))

            potential_win = any([x["potential_win"] for x in children_combinations])

        if try_move:
            clear_sqs(board, color ^ STONE, move["critical_sqs"])

    if not try_move:
        clear_sqs(board, color ^ STONE, move["critical_sqs"])

    clear_sqs(board, color, move["next_sqs"])

    return new_search_node(move, threats, potential_win, children)


# n = 10000

# for _ in range(n):
#     threat_space_search(state.board, state.turn)

# start = time.monotonic()
# for _ in range(n):
#     threat_space_search(state.board, state.turn)
# end = time.monotonic()
# print("Time taken: ", end - start, " seconds")

node = threat_space_search(state.board, state.turn, search_combinations=False)
for child in node["children"]:
    if child["potential_win"]:
        print(child["move"]["last_sqs"])
