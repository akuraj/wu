import numpy as np
from state import State
from utils import pattern_search
import time
from numba import njit

# Implement Pattern Class. And sub-class Threat? Direction as a property?
# Implement code to identify and return said pattern?

state = State()

a1 = np.array([1, 2, 3, 4, 5, 6])

for i in range(0, 6):
    state.board[0][i] = i + 1
    state.board[7][i + 6] = i + 1


@njit
def test_fn(board, pattern, n):
    tot = 0
    for _ in range(n):
        tot += pattern_search(board, pattern, 1)

    return tot


n = 1000000

test_fn(state.board, a1, n)

start = time.monotonic()

print(test_fn(state.board, a1, n))

end = time.monotonic()
print("Time taken: ", end - start, " seconds")
