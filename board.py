"""Functions related to the board and it's representation."""

import numpy as np
from numba import njit
from consts import (SIDE_LEN_ACT, SIDE_LEN, EMPTY, WALL, BLACK, WHITE, COLORS,
                    ACT_ELEMS_TO_CHRS, SPL_ELEM_CHR)


def row_idx_to_num(x):
    assert 1 <= x <= SIDE_LEN_ACT
    return SIDE_LEN_ACT + 1 - x


row_num_to_idx = row_idx_to_num


def col_idx_to_chr(x):
    assert 1 <= x <= SIDE_LEN_ACT
    return chr(ord("a") + x - 1)


def col_chr_to_idx(x):
    idx = ord(x) - ord("a") + 1
    assert 1 <= idx <= SIDE_LEN_ACT
    return idx


def point_to_algebraic(x):
    assert len(x) == 2
    row_num = row_idx_to_num(x[0])
    col_chr = col_idx_to_chr(x[1])
    return f"{col_chr}{row_num}"


def algebraic_to_point(x):
    col_idx = col_chr_to_idx(x[0])
    row_idx = row_num_to_idx(int(x[1:]))
    return (row_idx, col_idx)


@njit
def new_board():
    """Get new board."""

    board = np.full((SIDE_LEN, SIDE_LEN), EMPTY, dtype=np.byte)

    # Set the walls.
    for wall in (0, SIDE_LEN - 1):
        for i in range(SIDE_LEN):
            board[wall, i] = WALL
            board[i, wall] = WALL

    return board


def get_board(blacks, whites):
    """Get board from lists of points."""

    assert not set.intersection(set(blacks), set(whites))

    board = new_board()

    for elem in blacks:
        board[algebraic_to_point(elem)] = BLACK

    for elem in whites:
        board[algebraic_to_point(elem)] = WHITE

    return board


def board_to_str(board):
    """Representation of the board as a string."""

    board_repr = ""

    for i in range(board.shape[0]):
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

        for j in range(board.shape[1]):
            if board[i][j] in ACT_ELEMS_TO_CHRS:
                board_repr += ACT_ELEMS_TO_CHRS[board[i][j]]
            else:
                board_repr += SPL_ELEM_CHR

            board_repr += " "

        board_repr += "\n"

    board_repr += "     "

    for i in range(1, SIDE_LEN_ACT + 1):
        board_repr += col_idx_to_chr(i)
        board_repr += " "

    board_repr += "\n\n"

    return board_repr


@njit
def set_sq(board, color, point):
    """Sets given square on board to given color."""

    assert color in COLORS
    assert board[point] == EMPTY
    board[point] = color


@njit
def clear_sq(board, color, point):
    """Clears given square on board of given color."""

    assert color in COLORS
    assert board[point] == color
    board[point] = EMPTY
