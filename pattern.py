"""Define class to represent threat patterns, and related functions (search etc.)."""

from enum import IntEnum, auto, unique
from functools import reduce
import numpy as np
from consts import (GEN_ELEMS, EMPTY, DEFCON_RANGE, OWN, WALL_ENEMY,
                    NOT_OWN, GEN_ELEMS_TO_NAMES)
from geometry import point_set_on_line
from pattern_search import (search_board, search_point, search_point_own,
                            search_board_next_sq, search_point_next_sq,
                            search_point_own_next_sq, one_step_from_straight_threat,
                            degree, defcon_from_degree)


class Pattern:
    """Pattern: Used to represent threat patterns."""

    def __init__(self,
                 pattern,
                 critical_sqs,
                 name):
        # Make sure pattern has valid elements.
        for elem in pattern:
            assert elem in GEN_ELEMS
            assert elem == OWN or elem & OWN == 0

        # Critical Squares are the places where if the oppenent plays,
        # then the threat is mitigated.
        # Checks on critical_sqs.
        critical_sqs.sort()
        critical_sqs_uniq = list(set(critical_sqs))
        critical_sqs_uniq.sort()
        assert critical_sqs == critical_sqs_uniq
        allowed = range(len(pattern))
        for sq in critical_sqs:
            # sq must be EMPTY for it to be critical.
            assert sq in allowed and pattern[sq] == EMPTY

        # Check size of name.
        assert len(name) > 0

        # Check that any OWN or EMPTY squares in the pattern are contiguous,
        # i.e., OWN/EMPTY is not interrupted by any other kind of square.
        # This is what a normal/useful pattern would like.
        oe_start = False
        oe_end = False
        for v in pattern:
            if v in (OWN, EMPTY):
                if not oe_start:
                    oe_start = True

                if oe_end:
                    raise Exception("Non-contiguous OWN/EMPTY squares!")
            else:
                if oe_start and not oe_end:
                    oe_end = True

        self.pattern = np.array(pattern, dtype=np.byte)
        self.critical_sqs = np.array(critical_sqs, dtype=np.byte)
        self.own_sqs = np.array([i for i, v in enumerate(pattern) if v == OWN], dtype=np.byte)
        self.name = name
        self.index = -1  # Initialize index to -1.

        # Add entry for empty_sqs. critical_sqs appear first.
        other_empty_sqs = [i for i, v in enumerate(pattern) if v == EMPTY and i not in critical_sqs]
        self.empty_sqs = np.array(critical_sqs + other_empty_sqs, dtype=np.byte)

        # Add defcon.
        self.defcon = defcon_from_degree(degree(self.pattern))

        # Add "immediate" flag.
        self.immediate = True if self.defcon < 2 else one_step_from_straight_threat(self.pattern)

        # Checks on data fields.
        assert self.pattern.ndim == 1
        assert self.pattern.size > 0
        assert self.critical_sqs.ndim == 1
        assert self.own_sqs.ndim == 1
        assert self.empty_sqs.ndim == 1
        assert self.defcon in DEFCON_RANGE

        # Check on empty_sqs that they need to be useful.
        curr_degree = degree(self.pattern)
        for esq in self.empty_sqs:
            next_pattern = np.array(self.pattern, dtype=np.byte)
            next_pattern[esq] = OWN
            assert degree(next_pattern) == curr_degree + 1

    def __repr__(self):
        desc_list = [GEN_ELEMS_TO_NAMES[x] for x in self.pattern]
        return ("pattern: {0}\n"
                "defcon: {1}\n"
                "immediate: {2}\n"
                "critical_sqs: {3}\n"
                "own_sqs: {4}\n"
                "empty_sqs: {5}\n"
                "name: {6}\n"
                "index: {7}\n").format(str(desc_list),
                                       str(self.defcon),
                                       str(self.immediate),
                                       str(self.critical_sqs),
                                       str(self.own_sqs),
                                       str(self.empty_sqs),
                                       str(self.name),
                                       str(self.index))

    def __str__(self):
        return repr(self)


# *** PATTERN CONSTS ***

# Win pattern.
P_WIN = Pattern([OWN, OWN, OWN, OWN, OWN], [], "P_WIN")

# Threat patterns (including low priority threats).
P_4_ST = Pattern([EMPTY, OWN, OWN, OWN, OWN, EMPTY], [], "P_4_ST")
P_4_A = Pattern([WALL_ENEMY, OWN, OWN, OWN, OWN, EMPTY], [5], "P_4_A")
P_4_B = Pattern([NOT_OWN, OWN, OWN, OWN, EMPTY, OWN], [4], "P_4_B")
P_4_C = Pattern([NOT_OWN, OWN, OWN, EMPTY, OWN, OWN, NOT_OWN], [3], "P_4_C")
P_3_ST = Pattern([EMPTY, EMPTY, OWN, OWN, OWN, EMPTY, EMPTY], [1, 5], "P_3_ST")
P_3_A = Pattern([WALL_ENEMY, EMPTY, OWN, OWN, OWN, EMPTY, EMPTY], [1, 5, 6], "P_3_A")
P_3_B = Pattern([EMPTY, OWN, OWN, EMPTY, OWN, EMPTY], [0, 3, 5], "P_3_B")
P_3_C = Pattern([WALL_ENEMY, OWN, OWN, OWN, EMPTY, EMPTY], [4, 5], "P_3_C")
P_3_D = Pattern([WALL_ENEMY, OWN, OWN, EMPTY, OWN, EMPTY], [3, 5], "P_3_D")
P_3_E = Pattern([WALL_ENEMY, OWN, EMPTY, OWN, OWN, EMPTY], [2, 5], "P_3_E")
P_3_F = Pattern([WALL_ENEMY, EMPTY, OWN, OWN, OWN, EMPTY, WALL_ENEMY], [1, 5], "P_3_F")
P_3_G = Pattern([OWN, OWN, EMPTY, EMPTY, OWN], [2, 3], "P_3_G")
P_3_H = Pattern([OWN, EMPTY, OWN, EMPTY, OWN], [1, 3], "P_3_H")
P_2_A = Pattern([EMPTY, EMPTY, OWN, OWN, EMPTY, EMPTY], [0, 1, 4, 5], "P_2_A")
P_2_B = Pattern([EMPTY, EMPTY, OWN, EMPTY, OWN, EMPTY, EMPTY], [0, 1, 3, 5, 6], "P_2_B")
P_2_C = Pattern([EMPTY, OWN, EMPTY, EMPTY, OWN, EMPTY], [0, 2, 3, 5], "P_2_C")

# NOTE: Put all the patterns defined above in this list.
PATTERNS = [P_WIN, P_4_ST, P_4_A, P_4_B, P_4_C, P_3_ST, P_3_A, P_3_B,
            P_3_C, P_3_D, P_3_E, P_3_F, P_3_G, P_3_H,
            P_2_A, P_2_B, P_2_C]

# Setting indices of PATTERNS.
for i, p in enumerate(PATTERNS):
    p.index = i

NUM_PTNS = len(PATTERNS)

PATTERNS_BY_DEFCON = dict()
for p in PATTERNS:
    if p.defcon in PATTERNS_BY_DEFCON:
        PATTERNS_BY_DEFCON[p.defcon].append(p)
    else:
        PATTERNS_BY_DEFCON[p.defcon] = [p]

PATTERNS_BY_NAME = dict()
for p in PATTERNS:
    assert p.name not in PATTERNS_BY_NAME
    PATTERNS_BY_NAME[p.name] = p

# Immediate/High Priority PATTERNS.
PATTERNS_I = [x for x in PATTERNS if x.immediate]

# Low Priority PATTERNS.
PATTERNS_NI = [x for x in PATTERNS if not x.immediate]


# *** THREAT PRIORITY ENUM ***

@unique
class ThreatPri(IntEnum):
    """Enum to represent the priority of a Threat."""

    ALL = auto()
    IMMEDIATE = auto()
    NON_IMMEDIATE = auto()

# *** PATTERN SEARCH FUNCTIONS ***


def threat_item(match, pattern):
    """Threat: the where and the what."""

    return {"match": match,
            "pidx": pattern.index,
            "critical_sqs": point_set_on_line(match[0],
                                              match[1],
                                              pattern.critical_sqs)}


def get_patterns_with_pri(pri):
    """Get patterns with the given priority level."""

    if pri == ThreatPri.ALL:
        return PATTERNS
    elif pri == ThreatPri.IMMEDIATE:
        return PATTERNS_I
    elif pri == ThreatPri.NON_IMMEDIATE:
        return PATTERNS_NI
    else:
        raise Exception(f"Invalid priority: {pri}")


def search_all_board(board, color, pri):
    """Self explanatory."""

    return [threat_item(match, p)
            for p in get_patterns_with_pri(pri)
            for match in search_board(board, p.pattern, color)]


def search_all_point(board, color, point, pri):
    """Self explanatory."""

    return [threat_item(match, p)
            for p in get_patterns_with_pri(pri)
            for match in search_point(board, p.pattern, color, point)]


def search_all_point_own(board, color, point, pri):
    """Self explanatory."""

    return [threat_item(match, p)
            for p in get_patterns_with_pri(pri)
            for match in search_point_own(board, p.pattern, color, point, p.own_sqs)]


def search_all_points_own(board, color, points, pri, intersection=False):
    """Self explanatory."""

    matches_for_points = [search_all_point_own(board, color, x, pri) for x in points]

    all_matches_dict = dict()
    for matches in matches_for_points:
        for match in matches:
            key = (match["match"], match["pidx"])
            if key not in all_matches_dict:
                all_matches_dict[key] = match

    if intersection:
        keys_for_points = [{(x["match"], x["pidx"]) for x in matches}
                           for matches in matches_for_points]
        common_keys = reduce(set.intersection, keys_for_points)
        return [all_matches_dict[x] for x in common_keys]
    else:
        return list(all_matches_dict.values())


def search_all_board_get_next_sqs(board, color, pri):
    """Self explanatory."""

    return {x[0] for p in get_patterns_with_pri(pri)
            for x in search_board_next_sq(board, p.pattern, color)}


def search_all_point_get_next_sqs(board, color, point, pri):
    """Self explanatory."""

    return {x[0] for p in get_patterns_with_pri(pri)
            for x in search_point_next_sq(board, p.pattern, color, point)}


def search_all_point_own_get_next_sqs(board, color, point, pri):
    """Self explanatory."""

    return {x[0] for p in get_patterns_with_pri(pri)
            for x in search_point_own_next_sq(board, p.pattern, color, point, p.own_sqs)}
