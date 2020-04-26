"""A place for general TODOs."""

# *** Patterns and Threats; Pattern Matching ***
# TODO: Looking into what other pattern_search functions we need.
# TODO: We need at least the threats/(new threats?) generated by a given move.
# TODO: If two threats have the same exact critical squares,
#       then they can be handled by the same move(s). No need to dedupe them.
# TODO: Implement function to calculate intersection of pattern matches.
# TODO: Implement display/print for Pattern class (and any inheriting class).

# *** Threat Space Search ***
# TODO: What do we need here?

# *** Profiling and Testing ***
# TODO: Create tests and profiling fns for pattern_search.

# *** Consts ***
# TODO: Remove unnecessary constants.

# *** State Represenation ***
# TODO: Stricter check on win status to make sure no multiple wins for a given player?
# TODO: Implement display/print for State.
# TODO: Calculate and store Rich State?

# *** Performance Concerns ***
# TODO: Do we need to always get the side of the board? Can't we just assume it to be size?
# TODO: Inline numba jitted functions?
# TODO: Remove unnecessary asserts.

# *** Linting and Conventions ***
# TODO: Cleanup import statements.

# *** Standard Gomoku Implementation ***
# TODO: We can rely on the win pattern to differentiate between Standard and Freestyle.
# TODO: Specialize threats for Standard case.
# TODO: Control Freestyle or Standard via a global flag? Or better to do via State?
# TODO: Implement Standard Gomoku.

# *** Swap2 Implementation ***
# TODO: Implement Swap2 (and update state initialization, relevant checks, and code).
