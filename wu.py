"""Driver module."""

import time
from state import get_state
from threat_space_search import tss_board, potential_win_variations, animate_variation
from board import point_to_algebraic
from consts import BLACK


# state = get_state(["a1", "a2", "a3", "a13", "a14", "a15", "b1", "b15", "c1", "c15",
#                     "f14", "g13", "i9", "i10", "m1", "m15", "n1", "n15", "o1", "o2",
#                     "o3", "o13", "o14", "o15"],
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

# TODO: Profile threat space search!

n = 10

for _ in range(n):
    tss_board(state.board, state.turn)

start = time.monotonic()

for _ in range(n):
    tss_board(state.board, state.turn)

end = time.monotonic()
print("Time taken: ", end - start, " seconds")

# node = tss_board(state.board, state.turn)
# for child in node["children"]:
#     if child["potential_win"]:
#         print(child["next_sq"])

# win_vars = potential_win_variations(node)
# print(len(win_vars))

# variation = win_vars[0]
# animate_variation(state.board, state.turn, variation)
