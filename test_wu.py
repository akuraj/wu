from consts import SIDE_LEN, COLORS, NUM_DIRECTIONS
from pattern import PATTERNS
from utils import (new_board, get_pattern, is_symmetric, apply_pattern, increments,
                   search_board, search_point, search_point_own)


def test_truth():
    truth = True
    beauty = True

    assert truth == beauty, "How can this be?!"


def test_search_fns():
    for color in COLORS:
        for pattern_obj in PATTERNS:
            gen_pattern = pattern_obj.pattern
            own_sqs = pattern_obj.own_sqs
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

                            # search_board
                            matches = search_board(board, gen_pattern, color)
                            assert expected_matches == matches

                            # search_point
                            for k in range(length):
                                point = (i + row_inc * k, j + col_inc * k)
                                matches = search_point(board, gen_pattern, color, point)
                                assert expected_matches == matches

                            # search_point_own
                            for k in range(length):
                                point = (i + row_inc * k, j + col_inc * k)
                                matches = search_point_own(board,
                                                           gen_pattern,
                                                           color,
                                                           point,
                                                           own_sqs)

                                if pattern[k] == color:
                                    assert expected_matches == matches
                                else:
                                    expected_matches == []


def subtest_example():
    assert False
