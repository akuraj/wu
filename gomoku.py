import numpy as np
from state import State
from utils import pattern_search
import time

# Implement Pattern Class. And sub-class Threat? Direction as a property?
# Implement code to identify and return said pattern?

state = State()

a1 = np.array([1, 2, 3, 4, 5, 6])

n = 1000000

for _ in range(n):
    pattern_search(state.board, a1, 1)

start = time.monotonic()

for _ in range(n):
    pattern_search(state.board, a1, 1)

end = time.monotonic()
print("Time taken: ", end - start, " seconds")
