SIDE_LEN_ACT = 15
SIDE_LEN = SIDE_LEN_ACT + 2  # Including the walls.

# NOTE: All the actual elements defined below must be part of ACT_ELEMS,
#       as well as ACT_ELEMS_TO_CHRS and ACT_ELEMS_TO_NAMES.
EMPTY = 1 << 0
BLACK = 1 << 1
WHITE = 1 << 2
WALL = 1 << 3

ACT_ELEMS = [EMPTY, BLACK, WHITE, WALL]

ACT_ELEMS_TO_CHRS = dict()
ACT_ELEMS_TO_CHRS[EMPTY] = "+"
ACT_ELEMS_TO_CHRS[BLACK] = chr(9679)
ACT_ELEMS_TO_CHRS[WHITE] = chr(9675)
ACT_ELEMS_TO_CHRS[WALL] = " "
assert set(ACT_ELEMS_TO_CHRS.keys()) == set(ACT_ELEMS)
assert len(set(ACT_ELEMS_TO_CHRS.values())) == len(ACT_ELEMS)

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

# If defcon is x, then game will be over in x moves if no action is taken. 0 is game over.
DEFCON_RANGE = range(6)
