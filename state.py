from enum import IntEnum, auto, unique
import numpy as np
from consts import (SIDE_LEN, SIDE_LEN_ACT, EMPTY, BLACK, WHITE, WALL,
                    ACT_ELEMS_TO_CHRS, ACT_ELEMS_TO_NAMES, SPL_ELEM_CHR)
from utils import new_board, search_board, row_idx_to_num, col_idx_to_chr
from pattern import P_WIN


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
        board_repr = ""

        for i in range(self.board.shape[0]):
            num_str = "  "
            if 1 <= i <= SIDE_LEN_ACT:
                num_str = str(row_idx_to_num(i))
                if len(num_str) == 2:
                    pass
                elif len(num_str) == 1:
                    num_str = " " + num_str
                else:
                    raise Exception(f"Invalid index: {i}!")

            board_repr += num_str + " "

            for j in range(self.board.shape[1]):
                if self.board[i][j] in ACT_ELEMS_TO_CHRS:
                    board_repr += ACT_ELEMS_TO_CHRS[self.board[i][j]]
                else:
                    board_repr += SPL_ELEM_CHR

                board_repr += " "

            board_repr += "\n"

        board_repr += "     "

        for i in range(1, SIDE_LEN_ACT + 1):
            board_repr += col_idx_to_chr(i)
            board_repr += " "

        board_repr += "\n\n"

        return ("\nboard:\n{0}"
                "turn: {1}\n"
                "status: {2}\n").format(board_repr,
                                        ACT_ELEMS_TO_NAMES[self.turn],
                                        str(self.status))

    def __str__(self):
        return repr(self)
