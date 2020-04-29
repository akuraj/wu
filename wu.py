import numpy as np
import time
from state import State
from utils import pattern_search, pattern_search_incl, pattern_search_incl_2
from numba import njit
from consts import OWN, EMPTY, BLACK, WHITE, NOT_OWN, WALL
from pattern import P_3_B


state = State()
board = state.board

pattern = P_3_B.pattern
color = WHITE
point = (8, 8)
own_sqs = P_3_B.own_sqs

for i in P_3_B.own_sqs:
    board[point[0] - 2 + i][point[1] - 2 + i] = color
    board[point[0]][point[1] - 2 + i] = color
    board[point[0] - 2 + i][point[1]] = color

print(board)
print(pattern)


n = 1000000

print("\n")
print(pattern_search(board, pattern, color))


@njit
def test_fn(n):
    for _ in range(n):
        pattern_search(board, pattern, color)


test_fn(n)

start = time.monotonic()
test_fn(n)
end = time.monotonic()
print("Time taken: ", end - start, " seconds")


print("\n")
print(pattern_search_incl(board, pattern, color, point, own_sqs))


@njit
def test_fn_2(n):
    for _ in range(n):
        pattern_search_incl(board, pattern, color, point, own_sqs)


test_fn_2(n)

start = time.monotonic()
test_fn_2(n)
end = time.monotonic()
print("Time taken: ", end - start, " seconds")


print("\n")
print(pattern_search_incl_2(board, pattern, color, point))


@njit
def test_fn_3(n):
    for _ in range(n):
        pattern_search_incl_2(board, pattern, color, point)


test_fn_3(n)

start = time.monotonic()
test_fn_3(n)
end = time.monotonic()
print("Time taken: ", end - start, " seconds")