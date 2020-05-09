import numpy as np
import time
from state import State
from utils import (search_board, search_point, search_point_own,
                   search_board_next_sq, search_point_next_sq, search_point_own_next_sq,
                   get_pattern, apply_pattern)
from numba import njit
from consts import OWN, EMPTY, BLACK, WHITE, NOT_OWN, WALL
from pattern import P_3_B, P_4_ST, P_4_A
from test_wu import test_search_board


state = State()

board = state.board
pat_inst = P_3_B

gen_pattern = pat_inst.pattern

color = WHITE
point = (8, 8)

own_sqs = pat_inst.own_sqs

for i in own_sqs:
    board[point[0] - 2 + i][point[1] - 2 + i] = color
    board[point[0]][point[1] - 2 + i] = color
    board[point[0] - 2 + i][point[1]] = color

print(state)
print(P_3_B)

n = 10000000

print("\n")
# print(search_board(board, gen_pattern, color))
print(search_point(board, gen_pattern, color, point))
# print(search_point_own_next_sq(board, gen_pattern, color, point, own_sqs))


@njit
def test_fn(n):
    for _ in range(n):
        # search_board(board, gen_pattern, color)
        search_point(board, gen_pattern, color, point)
        # search_point_own_next_sq(board, gen_pattern, color, point, own_sqs)


test_fn(n)

start = time.monotonic()
test_fn(n)
end = time.monotonic()
print("Time taken: ", end - start, " seconds")
