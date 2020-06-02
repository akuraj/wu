"""Driver module."""

import time
# from numba import njit
from functools import reduce
from state import get_state
from utils import (new_search_node, new_move, MoveType, new_threat_seq_item,
                   potential_win_variations)
from board import set_sqs, clear_sqs, point_to_algebraic
from consts import BLACK, STONE
from pattern import (ThreatPri, search_all_board, search_all_point_own,
                     search_all_board_get_next_sqs,
                     search_all_point_own_get_next_sqs)


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

# state = get_state(["g10", "h8", "i7", "j7", "j9"],
#                   ["g7", "g8", "g9", "i9", "k8"],
#                   BLACK,
#                   True)

# state = get_state(["f6", "h6", "g7", "h7", "h8", "g11"],
#                   ["e5", "h5", "g6", "l6", "f7", "g8"],
#                   BLACK,
#                   True)

# state = get_state(["j5", "j6", "i10", "i11"],
#                   [],
#                   BLACK,
#                   False)

print(state)


def get_next_sqs_from_state(board, color, move, pri):
    if move["move_type"] == MoveType.NONE:
        return search_all_board_get_next_sqs(board, color, pri)
    elif move["move_type"] == MoveType.POINT:
        return search_all_point_own_get_next_sqs(board,
                                                 color,
                                                 move["last_sqs"][0],
                                                 pri)
    else:
        raise Exception("Invalid move type!")


# TODO: Profile threat space search!
def threat_space_search(board, color, move=new_move()):
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
        next_sqs = get_next_sqs_from_state(board, color, move, ThreatPri.ALL)

        children = [threat_space_search(board,
                                        color,
                                        new_move([[new_threat_seq_item(x)]]))
                    for x in next_sqs]
        potential_win = any([x["potential_win"] for x in children])

        # if not potential_win:
        #     next_sqs_other = get_next_sqs_from_state(board, color, move, ThreatPri.NON_IMMEDIATE)
        #     children_other = [threat_space_search(board,
        #                                           color,
        #                                           new_move([[new_threat_seq_item(x)]]))
        #                       for x in next_sqs_other]
        #     potential_win = any([x["potential_win"] for x in children_other])
        #     children.extend(children_other)

        if try_move:
            clear_sqs(board, color ^ STONE, move["critical_sqs"])

    if not try_move:
        clear_sqs(board, color ^ STONE, move["critical_sqs"])

    clear_sqs(board, color, move["next_sqs"])

    return new_search_node(move, threats, potential_win, children)


# n = 20

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
        print(child["move"]["last_sqs"])

win_vars = potential_win_variations(node)
print(len(win_vars))
# variation = [point_to_algebraic(x) for x in win_vars[10]]
# print(variation)
