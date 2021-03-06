"""Implements a class to represent State and related methods."""

from enum import IntEnum, auto, unique
import numpy as np
from consts import SIDE_LEN, EMPTY, BLACK, WHITE, WALL, COLORS, ACT_ELEMS_TO_NAMES
from pattern_search import search_board
from board import new_board, get_board, board_to_str
from pattern import P_WIN


@unique
class Status(IntEnum):
    """Enum to represent the current status."""

    ONGOING = auto()
    BLACK_WON = auto()
    WHITE_WON = auto()


class State:
    """Game State."""

    def __init__(self,
                 board=new_board(),
                 turn=BLACK,
                 strict_stone_count=True):

        # State Integrity Checks.
        assert board.shape == (SIDE_LEN, SIDE_LEN)
        assert turn in COLORS

        black_total = 0
        white_total = 0

        for (i, j), val in np.ndenumerate(board):
            if i in (0, SIDE_LEN - 1) or j in (0, SIDE_LEN - 1):
                assert val == WALL
            elif val == BLACK:
                black_total += 1
            elif val == WHITE:
                white_total += 1
            elif val == EMPTY:
                pass
            else:
                raise Exception(f"Invalid item on board: {val}")

        if strict_stone_count:
            if black_total == white_total + 1:
                assert turn == WHITE
            elif black_total == white_total:
                assert turn == BLACK
            else:
                raise Exception(f"""Invalid number of stones on the board:\
                                Black: {black_total}, White: {white_total}""")

        # Calculate game status.
        status = Status.ONGOING

        black_won = len(search_board(board, P_WIN.pattern, BLACK)) > 0
        white_won = len(search_board(board, P_WIN.pattern, WHITE)) > 0

        if black_won and white_won:
            raise Exception("Both BLACK and WHITE cannot have won!")
        elif black_won:
            status = Status.BLACK_WON
            assert turn == WHITE
        elif white_won:
            status = Status.WHITE_WON
            assert turn == BLACK

        # Copy onto self.
        self.board = np.copy(board.astype(np.byte))
        self.turn = turn
        self.status = status

    def __repr__(self):
        return ("\nboard:\n{0}"
                "turn: {1}\n"
                "status: {2}\n").format(board_to_str(self.board),
                                        ACT_ELEMS_TO_NAMES[self.turn],
                                        str(self.status))

    def __str__(self):
        return repr(self)


def get_state(blacks, whites, turn, strict_stone_count):
    """Return State object."""

    return State(get_board(blacks, whites), turn, strict_stone_count)
