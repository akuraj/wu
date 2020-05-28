"""Useful constants."""

SIDE_LEN_ACT = 15
SIDE_LEN = SIDE_LEN_ACT + 2  # Including the walls.

# NOTE: All the actual elements defined below must be part of ACT_ELEMS,
#       as well as ACT_ELEMS_TO_CHRS and ACT_ELEMS_TO_NAMES.
EMPTY = 1 << 0
BLACK = 1 << 1
WHITE = 1 << 2
WALL = 1 << 3

ACT_ELEMS = [EMPTY, BLACK, WHITE, WALL]

# Check that ACT_ELEMS are defined without mutual overlap.
NUM_ACT_ELEMS = len(ACT_ELEMS)
for i in range(NUM_ACT_ELEMS):
    for j in range(i + 1, NUM_ACT_ELEMS):
        assert ACT_ELEMS[i] & ACT_ELEMS[j] == 0

COLORS = (BLACK, WHITE)

BLACK_CIRCLE = chr(9679)
WHITE_CIRCLE = chr(9675)

# NOTE: Need to switch strone colors if you are using a dark theme in your console.
SWITCH_DISPLAY_COLORS = True

ACT_ELEMS_TO_CHRS = dict()
ACT_ELEMS_TO_CHRS[EMPTY] = "+"
ACT_ELEMS_TO_CHRS[BLACK] = WHITE_CIRCLE if SWITCH_DISPLAY_COLORS else BLACK_CIRCLE
ACT_ELEMS_TO_CHRS[WHITE] = BLACK_CIRCLE if SWITCH_DISPLAY_COLORS else WHITE_CIRCLE
ACT_ELEMS_TO_CHRS[WALL] = " "
assert set(ACT_ELEMS_TO_CHRS.keys()) == set(ACT_ELEMS)
assert len(set(ACT_ELEMS_TO_CHRS.values())) == len(ACT_ELEMS)
SPL_ELEM_CHR = "!"  # For printing non-standard elements. Useful for debugging.


ACT_ELEMS_TO_NAMES = dict()
ACT_ELEMS_TO_NAMES[EMPTY] = "EMPTY"
ACT_ELEMS_TO_NAMES[BLACK] = "BLACK"
ACT_ELEMS_TO_NAMES[WHITE] = "WHITE"
ACT_ELEMS_TO_NAMES[WALL] = "WALL"
assert set(ACT_ELEMS_TO_NAMES.keys()) == set(ACT_ELEMS)
assert len(set(ACT_ELEMS_TO_NAMES.values())) == len(ACT_ELEMS)

# NOTE: Generic Patterns are specified from BLACK's POV.
# NOTE: Allowed values include the below plus EMPTY and WALL (see GEN_ELEMS).
# NOTE: If you define a new generic element, please add it to GEN_ELEMS
#       as well as GEN_ELEMS_TO_NAMES.
OWN = BLACK
ENEMY = WHITE
STONE = OWN | ENEMY
ANY = EMPTY | STONE | WALL
NOT_EMPTY = ANY ^ EMPTY
NOT_WALL = ANY ^ WALL
NOT_STONE = ANY ^ STONE
NOT_OWN = ANY ^ OWN
WALL_ENEMY = WALL | ENEMY

GEN_ELEMS = [EMPTY, WALL, OWN, ENEMY, STONE, ANY, NOT_EMPTY, NOT_WALL,
             NOT_STONE, NOT_OWN, WALL_ENEMY]

GEN_ELEMS_TO_NAMES = dict()
GEN_ELEMS_TO_NAMES[EMPTY] = "EMPTY"
GEN_ELEMS_TO_NAMES[WALL] = "WALL"
GEN_ELEMS_TO_NAMES[OWN] = "OWN"
GEN_ELEMS_TO_NAMES[ENEMY] = "ENEMY"
GEN_ELEMS_TO_NAMES[STONE] = "STONE"
GEN_ELEMS_TO_NAMES[ANY] = "ANY"
GEN_ELEMS_TO_NAMES[NOT_EMPTY] = "NOT_EMPTY"
GEN_ELEMS_TO_NAMES[NOT_WALL] = "NOT_WALL"
GEN_ELEMS_TO_NAMES[NOT_STONE] = "NOT_STONE"
GEN_ELEMS_TO_NAMES[NOT_OWN] = "NOT_OWN"
GEN_ELEMS_TO_NAMES[WALL_ENEMY] = "WALL_ENEMY"
assert set(GEN_ELEMS_TO_NAMES.keys()) == set(GEN_ELEMS)
assert len(set(GEN_ELEMS_TO_NAMES.values())) == len(GEN_ELEMS)

NUM_DIRECTIONS = 8

WIN_LENGTH = 5  # Length of a winning sequence.

# Some things implicitly assume a win length of 5, for example, threat pattern definitions.
# Don't change WIN_LENGTH without making all other relevant changes everywhere else in the project.
assert WIN_LENGTH == 5

# If defcon is x, then game will be over in x moves if no action is taken. 0 is game over.
# Effectively, the maximum distance away from winning.
MAX_DEFCON = WIN_LENGTH
DEFCON_RANGE = range(MAX_DEFCON + 1)
