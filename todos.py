"""A place for general TODOs."""

# *** TODO SOON ***
# TODO: Test the search functions.

# *** Patterns and Threats; Pattern Matching ***
# TODO: What other pattern search functions do we need?
# TODO: Add check on patterns containing only EMPTY, OWN squares in the middle?
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
# TODO: Use all patterns to assign a value to the position.
# TODO: null-move heuristic to see any short-term attacks?

# *** Profiling and Testing ***
# TODO: Create unit tests for relevant fns.
# TODO: Create profiling code for pattern search fns.

# *** Consts ***
# TODO: Remove unnecessary constants.

# *** State Represenation ***
# TODO: Stricter check on win status to make sure no multiple wins for a given player?
# TODO: Calculate and store Rich State?

# *** Performance Concerns ***
# TODO: Remove unnecessary asserts/checks/if. [IMPORTANT].
# TODO: Deduping the results of the point->next search is actually necessary?
# TODO: Check out numba features other than njit to speed up code!
# TODO: JIT Compile relevant classes using numba's jitclass.
#       Can speed up relevant loops (over patterns) by 30%.
# TODO: Inline numba jitted functions?

# *** Linting and Conventions ***
# TODO: Cleanup import statements.

# *** Standard Gomoku Implementation ***
# TODO: We can rely on the win pattern to differentiate between Standard and Freestyle.
# TODO: Specialize threats for Standard case.
# TODO: Control Freestyle or Standard via a global flag? Or better to do via State?
# TODO: Implement Standard Gomoku.

# *** Swap2 Implementation ***
# TODO: Implement Swap2 (and update state initialization, relevant checks, and code).

# *** Cleanup ***
# TODO: Remove unused functions (search related etc.).

# *** Release! ***
# TODO: Implement setup.py or pyproject.toml!
