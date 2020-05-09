from consts import SIDE_LEN, COLORS, NUM_DIRECTIONS
from pattern import PATTERNS
from utils import (new_board, get_pattern, is_symmetric, apply_pattern,
                   search_board, increments)

gen_patterns = [x.pattern for x in PATTERNS]


def test_truth():
    truth = True
    beauty = True

    assert truth == beauty, "How can this be?!"


def test_search_board():
    for color in COLORS:
        for gen_pattern in gen_patterns:
            pattern = get_pattern(gen_pattern, color)
            length = pattern.size
            symmetric = is_symmetric(pattern)
            ndirs = int(NUM_DIRECTIONS / 2) if symmetric else NUM_DIRECTIONS

            for i in range(SIDE_LEN):
                for j in range(SIDE_LEN):
                    for d in range(ndirs):
                        board = new_board()
                        if apply_pattern(board, pattern, (i, j), d):
                            (row_inc, col_inc) = increments(d)
                            start = (i, j)
                            end = (i + row_inc * (length - 1), j + col_inc * (length - 1))
                            expected_matches = [(start, end)]

                            matches = search_board(board, gen_pattern, color)

                            assert expected_matches == matches
