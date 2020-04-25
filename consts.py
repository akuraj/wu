SIDE_LEN_ACT = 15
SIDE_LEN = SIDE_LEN_ACT + 2  # Including the walls.

EMPTY = 1 << 0
BLACK = 1 << 1
WHITE = 1 << 2
WALL = 1 << 3

# NOTE: Generic Patterns are specified from BLACK's POV.
# NOTE: Allowed values include the below plus EMPTY and WALL (see GEN_ELEMS).
# NOTE: If you define a new generic element, please add it to GEN_ELEMS as well.
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

NUM_DIRECTIONS = 8

# If defcon is x, then game will be over in x moves if no action is taken. 0 is game over.
DEFCON_RANGE = range(6)
