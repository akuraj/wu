from consts import SIDE_LEN, COLORS, NUM_DIRECTIONS
from pattern import PATTERNS
from utils import (new_board, get_pattern, apply_pattern, increments,
                   point_is_on_line, matches_are_equal,
                   search_board, search_point, search_point_own,
                   search_board_next_sq, search_point_next_sq, search_point_own_next_sq,
                   assert_nb)
from numba import njit


def test_truth():
    truth = True
    beauty = True

    assert_nb(truth == beauty, "How can this be?!")


@njit
def subtest_search_board(board, gen_pattern, color, expected_matches):
    matches = search_board(board, gen_pattern, color)
    assert_nb(matches_are_equal(matches, expected_matches))


@njit
def subtest_search_point(board, gen_pattern, color,
                         start, end, expected_matches):
    for x in range(SIDE_LEN):
        for y in range(SIDE_LEN):
            point = (x, y)
            matches = search_point(board, gen_pattern, color, point)

            if point_is_on_line(point, start, end, True):
                assert_nb(matches_are_equal(matches, expected_matches))
            else:
                assert_nb(len(matches) == 0)


@njit
def subtest_search_point_own(board, gen_pattern, color, own_sqs,
                             start, end, expected_matches):
    for x in range(SIDE_LEN):
        for y in range(SIDE_LEN):
            point = (x, y)
            matches = search_point_own(board, gen_pattern, color, point, own_sqs)

            if point_is_on_line(point, start, end, True):
                if board[point] == color:
                    assert_nb(matches_are_equal(matches, expected_matches))
                else:
                    assert_nb(len(matches) == 0)
            else:
                assert_nb(len(matches) == 0)


@njit
def subtest_search_fns(gen_pattern, color, own_sqs):
    pattern = get_pattern(gen_pattern, color)
    length = pattern.size

    for i in range(SIDE_LEN):
        for j in range(SIDE_LEN):
            for d in range(NUM_DIRECTIONS):
                board = new_board()
                if apply_pattern(board, pattern, (i, j), d):
                    (row_inc, col_inc) = increments(d)
                    start = (i, j)
                    end = (i + row_inc * (length - 1), j + col_inc * (length - 1))
                    expected_matches = [(start, end)]

                    subtest_search_board(board, gen_pattern, color,
                                         expected_matches)
                    subtest_search_point(board, gen_pattern, color,
                                         start, end, expected_matches)
                    subtest_search_point_own(board, gen_pattern, color, own_sqs,
                                             start, end, expected_matches)


def test_search_fns():
    for color in COLORS:
        for pattern in PATTERNS:
            subtest_search_fns(pattern.pattern, color, pattern.own_sqs)
