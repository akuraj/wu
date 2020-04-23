import numpy as np
from state import State
from utils import pattern_search
import time
from numba import njit

# Implement Pattern Class. And sub-class Threat? Direction as a property?
# Implement code to identify and return said pattern?

state = State()

a1 = np.array([0, 1, 1, 1, 1, -1], dtype=np.byte)

for i in range(0, 4):
    state.board[0][10 + i] = 1

state.board[0][14] = -1

print(pattern_search(state.board, a1, 1, True))

@njit
def test_fn(board, pattern, n):
    for _ in range(n):
        pattern_search(board, pattern, 1, True)

n = 1000000
test_fn(state.board, a1, n)

start = time.monotonic()
test_fn(state.board, a1, n)
end = time.monotonic()

print("Time taken: ", end - start, " seconds")
