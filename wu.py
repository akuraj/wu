import numpy as np
import time
from state import get_state
from utils import (search_board, search_point, search_point_own,
                   search_board_next_sq, search_point_next_sq, search_point_own_next_sq,
                   get_pattern, apply_pattern, assert_nb)
from numba import njit
from consts import OWN, EMPTY, BLACK, WHITE, NOT_OWN, WALL
# from pattern import P_3_B, P_4_ST, P_4_A, PATTERNS_BY_DEFCON


state = get_state(["a1", "a2", "a3", "a13", "a14", "a15", "b1", "b15", "c1", "c15",
                   "f14", "g13", "i9", "i10", "m1", "m15", "n1", "n15", "o1", "o2",
                   "o3", "o13", "o14", "o15"],
                  ["i6", "i13", "j10"],
                  BLACK,
                  False)

print(state)

# start = time.monotonic()

# end = time.monotonic()
# print("Time taken: ", end - start, " seconds")
