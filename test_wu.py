from numba import njit
from consts import SIDE_LEN, COLORS, NUM_DIRECTIONS, EMPTY
from pattern import PATTERNS
from utils import (new_board, get_pattern, apply_pattern, increments,
                   point_is_on_line, matches_are_equal,
                   search_board, search_point, search_point_own,
                   search_board_next_sq, search_point_next_sq, search_point_own_next_sq,
                   assert_nb, next_sq_matches_are_subset)


@njit
def test_truth():
    truth = True
    beauty = True

    assert_nb(truth == beauty, "How can this be?!")


@njit
def subtest_search_board(board, gen_pattern, color, start, end):
    expected_matches = [(start, end)]
    matches = search_board(board, gen_pattern, color)
    assert_nb(matches_are_equal(matches, expected_matches))


@njit
def subtest_search_point(board, gen_pattern, color, start, end):
    expected_matches = [(start, end)]
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
                             start, end):
    expected_matches = [(start, end)]
    for x in range(SIDE_LEN):
        for y in range(SIDE_LEN):
            point = (x, y)
            matches = search_point_own(board, gen_pattern, color, point, own_sqs)

            if board[point] == color and point_is_on_line(point, start, end, True):
                assert_nb(matches_are_equal(matches, expected_matches))
            else:
                assert_nb(len(matches) == 0)


@njit
def subtest_search_board_next_sq(board, gen_pattern, color, own_sqs,
                                 start, end, d):
    (i, j) = start
    (row_inc, col_inc) = increments(d)

    for own_sq in own_sqs:
        test_sq = (i + row_inc * own_sq, j + col_inc * own_sq)
        expected_ns_matches = [(test_sq, (start, end))]

        stored_val = board[test_sq]
        board[test_sq] = EMPTY
        ns_matches = search_board_next_sq(board, gen_pattern, color)
        board[test_sq] = stored_val

        # We can only assert that naively expected matches are a subset of actual.
        assert_nb(next_sq_matches_are_subset(expected_ns_matches, ns_matches))

        # All matches must lie on the same line as the pattern.
        for nsm in ns_matches:
            assert_nb(point_is_on_line(nsm[0], start, end, False))


@njit
def subtest_search_point_next_sq(board, gen_pattern, color, own_sqs,
                                 start, end, d):
    (i, j) = start
    (row_inc, col_inc) = increments(d)

    for own_sq in own_sqs:
        test_sq = (i + row_inc * own_sq, j + col_inc * own_sq)
        expected_ns_matches = [(test_sq, (start, end))]

        for x in range(SIDE_LEN):
            for y in range(SIDE_LEN):
                point = (x, y)

                stored_val = board[test_sq]
                board[test_sq] = EMPTY
                ns_matches = search_point_next_sq(board, gen_pattern, color, point)
                board[test_sq] = stored_val

                # We can only assert that naively expected matches are a subset of actual,
                # if the point lies on the segment of the pattern.
                if point_is_on_line(point, start, end, True):
                    assert_nb(next_sq_matches_are_subset(expected_ns_matches, ns_matches))
                elif point_is_on_line(point, start, end, False):
                    pass
                else:
                    assert_nb(len(ns_matches) == 0)

                # All matches must lie on the same line as the pattern.
                for nsm in ns_matches:
                    assert_nb(point_is_on_line(nsm[0], start, end, False))


@njit
def subtest_search_point_own_next_sq(board, gen_pattern, color, own_sqs,
                                     start, end, d):
    (i, j) = start
    (row_inc, col_inc) = increments(d)

    for own_sq in own_sqs:
        test_sq = (i + row_inc * own_sq, j + col_inc * own_sq)
        expected_ns_matches = [(test_sq, (start, end))]

        for x in range(SIDE_LEN):
            for y in range(SIDE_LEN):
                point = (x, y)

                stored_val = board[test_sq]
                board[test_sq] = EMPTY
                ns_matches = search_point_own_next_sq(board, gen_pattern, color,
                                                      point, own_sqs)
                point_is_own_sq = board[point] == color
                board[test_sq] = stored_val

                # We can only assert that naively expected matches are a subset of actual,
                # if the point lies on the segment of the pattern.
                if point_is_own_sq and point_is_on_line(point, start, end, True):
                    assert_nb(next_sq_matches_are_subset(expected_ns_matches, ns_matches))
                elif point_is_own_sq and point_is_on_line(point, start, end, False):
                    pass
                else:
                    assert_nb(len(ns_matches) == 0)

                # All matches must lie on the same line as the pattern.
                for nsm in ns_matches:
                    assert_nb(point_is_on_line(nsm[0], start, end, False))


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

                    subtest_search_board(board, gen_pattern, color, start, end)
                    subtest_search_point(board, gen_pattern, color, start, end)
                    subtest_search_point_own(board, gen_pattern, color, own_sqs,
                                             start, end)

                    subtest_search_board_next_sq(board, gen_pattern, color, own_sqs,
                                                 start, end, d)
                    subtest_search_point_next_sq(board, gen_pattern, color, own_sqs,
                                                 start, end, d)
                    subtest_search_point_own_next_sq(board, gen_pattern, color, own_sqs,
                                                     start, end, d)


def test_search_fns():
    for color in COLORS:
        for pattern in PATTERNS:
            subtest_search_fns(pattern.pattern, color, pattern.own_sqs)
