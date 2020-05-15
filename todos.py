"""A place for general TODOs."""

# *** TODO SOON ***
# TODO: Write code for combination of two searches, or multiple as well?
# TODO: Can combine pairs by maintaining gain and cost squares upto relevant point,
#       and comparing the cumulative sets will determine if the points are in conflict or not.
# TODO: Traverse graph without recursion to make fns faster?
# TODO: Introduce a max-depth for combination searches in TSS?
# TODO: Make search node and threat item classes to make access faster?
# TODO: Figure out appropriate tree data structure for TSS.
# TODO: Implement dependency and conflict checks for TSS tree.
# TODO: Implement process/algo to combine useful sets of independent TSS trees.
# TODO: Cleanup/reorg/remove the rich data structures in state as needed.
# TODO: Remove unnecessary functions that were recently added.
# TODO: Remove unnecessary fields from threat data.
# TODO: Estimate impact of njit by turning it off to see if it's actually useful.
# TODO: Is jitting small functions actually helpful?
# TODO: Take point as a tuple and not two separate arguments!
# TODO: Transposition Table?
# TODO: Find all potential wins instead of just breaking at the first one we find?
# TODO: Test rich state and incremental update.
# TODO: Dedupe stored threats?
# TODO: What happens to rich state when we set multiple squares of opponent during TSS?

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
# TODO: Use all patterns to assign a value to the position.
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
