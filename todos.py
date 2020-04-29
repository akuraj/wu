"""A place for general TODOs."""

# *** Patterns and Threats; Pattern Matching ***
# TODO: Implement a list, as well, as a dict (keyed by defcon)
#       to access/enumerate all patterns.
# TODO: Test the search functions.
# TODO: Looking into what other pattern_search functions we need.
# TODO: Add check on patterns containing only EMPTY, OWN squares in the middle?
# TODO: If two threats have the same exact critical squares,
#       then they can be handled by the same move(s). No need to dedupe them.
# TODO: Implement function to calculate intersection of pattern matches.
# TODO: Implement display/print for Pattern class (and any inheriting class).
# TODO: Refactor common code in the "search*" functions.

# *** Threat Space Search ***
# TODO: What do we need here?

# *** Profiling and Testing ***
# TODO: Create unit tests for relevant fns.
# TODO: Add Travis CI to project.
# TODO: Create profiling code for pattern search fns.

# *** Consts ***
# TODO: Remove unnecessary constants.

# *** State Represenation ***
# TODO: Stricter check on win status to make sure no multiple wins for a given player?
# TODO: Implement display/print for State.
# TODO: Calculate and store Rich State?

# *** Performance Concerns ***
# TODO: Remove unnecessary asserts/checks/if. [IMPORTANT].
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
