import numpy as np
from consts import (SIDE_LEN, SIDE_LEN_ACT, EMPTY, BLACK, WHITE, WALL, COLORS,
                    ACT_ELEMS_TO_CHRS, ACT_ELEMS_TO_NAMES, SPL_ELEM_CHR, STONE)
from utils import (new_board, search_board, row_idx_to_num, col_idx_to_chr, get_board,
                   set_sq, clear_sq, del_threats_at_point, status_str, has_won)
from pattern import (P_WIN, search_all_board, search_all_board_next_sq,
                     search_all_point, search_all_point_next_sq)


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

        # Copy onto self.
        self.board = np.copy(board.astype(np.byte))
        self.turn = turn

        # Initialize rich state (threats, threats_next_sq).
        self.threats = {color: search_all_board(self.board, color)
                        for color in COLORS}
        self.threats_next_sq = {color: search_all_board_next_sq(self.board, color)
                                for color in COLORS}

        # Update status.
        self.status = EMPTY
        self.update_status()

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
                                        status_str(self.status))

    def __str__(self):
        return repr(self)

    def update_rich_state(self, point):
        for color in COLORS:
            del_threats_at_point(self.threats[color], point)
            self.threats[color].extend(search_all_point(self.board, color, point))

            del_threats_at_point(self.threats_next_sq[color], point)
            self.threats_next_sq[color].extend(search_all_point_next_sq(self.board,
                                                                        color,
                                                                        point))

    def update_status(self):
        status = EMPTY
        num_won = 0

        for color in COLORS:
            if has_won(self.threats[color]):
                status = color
                num_won += 1

        assert num_won <= 1
        assert status != self.turn
        self.status = status

    def make(self, point):
        assert self.status == EMPTY
        set_sq(self.board, self.turn, point)
        self.turn ^= STONE
        self.update_rich_state(point)
        self.update_status()

    def unmake(self, point):
        self.turn ^= STONE
        clear_sq(self.board, self.turn, point)
        self.update_rich_state(point)
        self.update_status()
        assert self.status == EMPTY


def get_state(blacks, whites, turn, strict_stone_count):
    return State(get_board(blacks, whites), turn, strict_stone_count)
