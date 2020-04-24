import numpy as np
import time
from state import State
from utils import pattern_search
from numba import njit
from consts import OWN, EMPTY, BLACK, WHITE, NOT_OWN


state = State()
# pattern = np.array([EMPTY, OWN, OWN, OWN, OWN, NOT_OWN], dtype=np.byte)
pattern = np.array([NOT_OWN, OWN, OWN, OWN, OWN, NOT_OWN], dtype=np.byte)
color = WHITE

for i in range(0, 4):
    state.board[1][11 + i] = color
    state.board[15 - i][12 + i] = color
    state.board[15 - i][15 - i] = color

print(state.board)
print(pattern)
print(pattern_search(state.board, pattern, color))


@njit
def test_fn(board, pattern, n):
    for _ in range(n):
        pattern_search(board, pattern, color)


n = 1000000
test_fn(state.board, pattern, n)

start = time.monotonic()
test_fn(state.board, pattern, n)
end = time.monotonic()

print("Time taken: ", end - start, " seconds")