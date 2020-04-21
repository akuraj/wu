from consts import BOARD_SIZE, EMPTY, BLACK, WHITE
import numpy as np


class State:
    """Game State."""

    # TODO: Implement Swap2 (and update relevant checks and code).
    # TODO: Implement Standard Gomoku.

    def __init__(self,
                 board=np.full((BOARD_SIZE, BOARD_SIZE), 0, dtype=np.byte),
                 turn=BLACK):

        # State Integrity Checks.
        assert board.shape == (BOARD_SIZE, BOARD_SIZE)
        assert turn == BLACK or turn == WHITE

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

        if black_total == white_total + 1:
            assert turn == WHITE
        elif black_total == white_total:
            assert turn == BLACK
        else:
            raise Exception(f"""Invalid number of stones on the board:\
                            Black: {black_total}, White: {white_total}""")

        # TODO: Calculate Game Status (ongoing, over etc.).

        # Copy input state onto self.
        self.board = np.copy(board)
        self.turn = turn

        # TODO: Calculate and store rich state.
