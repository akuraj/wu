import numpy as np
from consts import SIDE_LEN, EMPTY, BLACK, WHITE, WALL
from utils import new_board


class State:
    """Game State."""

    # TODO: Implement Swap2 (and update relevant checks and code).
    # TODO: Implement Standard Gomoku.

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

        # TODO: Calculate Game Status (ongoing, over etc.).

        # Copy input state onto self.
        self.board = np.copy(board.astype(np.byte))
        self.turn = turn

        # TODO: Calculate and store rich state.
