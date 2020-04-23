# TODO: Can we make use of enums for some of the groups of constants defined in this file?

SIDE_LEN_ACT = 15
SIDE_LEN = SIDE_LEN_ACT + 2  # Including the walls.

# TODO: Different values for below?
EMPTY = 0
BLACK = -1
WHITE = 1
WALL = 2
OWN = 3  # Represents an own stone in a generic pattern.
OPP = 4  # Represents an enemy stone in a generic pattern.
OPW = 5  # Represents an enemy stone or a wall in a generic pattern.
EOW = 6  # Represents an empty space, enemy stone or a wall in a generic pattern.

NUM_DIRECTIONS = 8
