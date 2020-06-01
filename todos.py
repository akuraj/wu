"""A place for general TODOs."""

# *** TODO SOON ***
# TODO: Check that listed patterns fully cover all possibilities.
#       Verify that there are no holes.
# TODO: FIXME: Too many garbage variations!
#       1) Can play LowPri threat as long as the move also generates a HighPri threat!
#       2) Search LowPri threats only if no win found via HighPri threats? Or always?
#       3) Stop searching children if a win is found? Or find all possible wins?
#       4) Stop searching and return False if opponent is winning via critical squares?
#          Under what conditions do we assume that opponent is winning?
#       5) Drop the combinations idea in favor of the LowPri idea?
#       6) Only store winning variations to help save space!
#       7) Sort win variations by length? Shorter is better.
#       7) Implement a transposition table. How do we cope with having different last_sqs?
#          A Zobrit hash?
#          A hash that depends on position as well as latest move?
#       8) What's the correct/viable TSS impl according to the paper? How does mine compare?
#       9) Max-depth for certain/all kinds of TSS?
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

# *** TODO SOONISH ***
# TODO: When getting next_sqs from node, also get path as well as cumulative gain and cost sqs.
#       That should make it more convenient to get compatible pairs/combinations.
# TODO: Write code for combination of two searches, or multiple as well?
# TODO: Can combine pairs by maintaining gain and cost squares upto relevant point,
#       and comparing the cumulative sets will determine if the points are in conflict or not.
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
