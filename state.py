import numpy as np
from consts import SIDE_LEN, EMPTY, BLACK, WHITE, WALL
from utils import new_board, pattern_search
from pattern import P_WIN
from enum import IntEnum, auto, unique


@unique
class Status(IntEnum):
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
        assert turn in (BLACK, WHITE)

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

        black_won = len(pattern_search(board, P_WIN.pattern, BLACK)) > 0
        white_won = len(pattern_search(board, P_WIN.pattern, WHITE)) > 0

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
