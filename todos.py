"""A place for general TODOs."""

# *** TODO SOON ***
# TODO: Cleanup pattern.py
# TODO: Refactor utils code into separate modules!!!
# TODO: Fix dangerous defaults!
# TODO: Print variations and search nodes in algebraic notation.
# TODO: Are we searching too wide/too deep? Should we stop a loop if a win is found?
#       Is it valuable to find all potential wins by searching all children?
# TODO: Add function to inspect or pretty print winning variations in node.
# TODO: Use this priority flag to decide what to do next w.r.t to critical sqs etc.?
#       You can play a low priority threat connected to last move,
#       as long as that move also generates a high priority threat!
# TODO: Check all test positions in paper. Implement regtests based on them.
# TODO: Finalize idea/format of combinations.
# TODO: Need function to search using a given sets of points as own sqs!
#       Something efficient and proper, not some hack.
# TODO: My TSS search tree differs from the one described in the book.
#       Reconcile/justify differences or change it. Make it better.
# TODO: Update searches for "all patterns".
#       Create an enum to represent searching for high, low or all priorities.
# TODO: If no threats are generated by point, should we look further?
#       What about no threats in case of combination?
# TODO: Need fn to search along direction at point?
# TODO: Function documentation!

# *** TODO SOONISH ***
# TODO: When getting next_sqs from node, also get path as well as cumulative gain and cost sqs.
#       That should make it more convenient to get compatible pairs/combinations.
# TODO: Write code for combination of two searches, or multiple as well?
# TODO: Can combine pairs by maintaining gain and cost squares upto relevant point,
#       and comparing the cumulative sets will determine if the points are in conflict or not.
# TODO: Introduce a max-depth for combination searches in TSS?
# TODO: Make search node and threat item classes to make access faster?
# TODO: Figure out appropriate tree data structure for TSS.
# TODO: Implement dependency and conflict checks for TSS tree.
# TODO: Implement process/algo to combine useful sets of independent TSS trees.
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
