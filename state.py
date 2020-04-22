import numpy as np
from consts import BOARD_SIDE, EMPTY, BLACK, WHITE


class State:
    """Game State."""

    # TODO: Implement Swap2 (and update relevant checks and code).
    # TODO: Implement Standard Gomoku.

    def __init__(self,
                 board=np.full((BOARD_SIDE, BOARD_SIDE), 0, dtype=np.byte),
                 turn=BLACK,
                 strict_stone_count=True):

        # State Integrity Checks.
        assert board.shape == (BOARD_SIDE, BOARD_SIDE)
        assert turn in (BLACK, WHITE)

        black_total = 0
        white_total = 0
        for val in np.nditer(board):
            if val == BLACK:
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
