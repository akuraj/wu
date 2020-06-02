"""A place for general TODOs."""

# *** TODO SOON ***
# TODO: FIXME: Too many garbage variations when using LowPri threats!
#       1) Can play LowPri threat as long as the move also generates a HighPri threat!
#       2) Search LowPri threats only if no win found via HighPri threats? Or always?
#       3) Only search LowPri threats a max number of ply in a given variation!
#          We can control this via a LowPriMaxDepth(?) variable.
#       4) Stop searching children if a win is found? Or find all possible wins?
#       5) Stop searching and return False if opponent is winning via critical squares?
#          Under what conditions do we assume that opponent is winning?
#       6) Only store winning variations to help save space!
#       7) Sort win variations by length? Shorter is better.
#       8) Implement a transposition table. How do we cope with having different last_sqs?
#          A Zobrit hash? Or just use a dict? What's the most efficient data structure?
#          A hash that depends on position as well as latest move?
#       9) What's the correct/viable TSS impl according to the paper? How does mine compare?
#       10) Max-depth for certain/all kinds of TSS?
#       11) Threats data and other data should be lean to reduce memory usage.
#       12) We don't actually need critical sqs for NON_IMMEDIATE threats.
#           Should we keep them as they are currently?
# TODO: Use Yixin to check for best moves in test positions.
#       Use it to guide the development effort and debugging.
# TODO: Check all test positions in paper. Implement regtests based on them.
# TODO: Print variations and search nodes in algebraic notation.
# TODO: Animate a variation.
# TODO: Refactor utils code into separate modules!!!
# TODO: Remove unnecessary fields from threat data.
# TODO: Fix dangerous defaults!
# TODO: Add function to inspect or pretty print winning variations in node.
# TODO: Need function to search using a given sets of points as own sqs!
#       Something efficient and proper, not some hack.
# TODO: Need fn to search along direction at point?
# TODO: Function documentation!
# TODO: Can we have a better way to input position?
# TODO: Remove unnecessary functions.

# *** TODO SOONISH ***
# TODO: Estimate impact of njit by turning it off to see if it's actually useful.
# TODO: Is jitting small functions actually helpful?
# TODO: Take point as a tuple and not two separate arguments!

# *** Patterns and Threats; Pattern Matching ***
# TODO: What other pattern search functions do we need?
# TODO: If two threats have the same exact critical squares,
#       then they can be handled by the same move(s). No need to dedupe them.
# TODO: Implement function to calculate intersection of pattern matches.

# *** Threat Space Search (TSS) ***
# TODO: What do we need here?

# *** Negamax Search ***
# TODO: Search Threat Space fully (FTSS) in an accurate manner,
#       instead of being too conservative like TSS?
# TODO: Implement an evaluation scale.
# TODO: Use Positional Evaluation for quiet/positions not determined by FTSS.

# *** Position Evaluation (Static/Semi-Static) ***
# TODO: Extend patterns to allow for non-threat patterns (2 in a row for example)?
# TODO: Use all patterns to assign a value to the position (including P_2_D?).
# TODO: null-move heuristic to see any short-term attacks?

# *** Profiling and Testing ***
# TODO: Create tests for algebraic related fns, state construction etc.
# TODO: Create profiling code for pattern search fns.

# *** Cleanup ***
# TODO: Remove unused functions (search related etc.).
# TODO: Remove unnecessary constants.
# TODO: Code organization: refactor utils to separate libs?

# *** State Represenation ***
# TODO: Stricter check on win status to make sure no multiple wins for a given player?
# TODO: Implement code to update status after move is made!
# TODO: Calculate and store Rich State?

# *** Performance Concerns ***
# TODO: Remove unnecessary asserts/checks/if. [IMPORTANT].
# TODO: Check out numba features other than njit to speed up code!
# TODO: Inline numba jitted functions?

# *** Linting and Conventions ***
# TODO: Add more documentation; consult pylint code conventions.
# TODO: Cleanup import statements.

# *** Standard Gomoku Implementation ***
# TODO: We can rely on the win pattern to differentiate between Standard and Freestyle.
# TODO: Specialize threats for Standard case.
# TODO: Control Freestyle or Standard via a global flag? Or better to do via State?
# TODO: Implement Standard Gomoku.

# *** Swap2 Implementation ***
# TODO: Implement Swap2 (and update state initialization, relevant checks, and code).

# *** Release! ***
# TODO: Implement setup.py or pyproject.toml!
