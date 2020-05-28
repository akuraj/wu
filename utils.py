from enum import IntEnum, auto, unique
from numba import njit
from consts import EMPTY, WIN_LENGTH, OWN, MAX_DEFCON
from geometry import (is_normal_line, chebyshev_distance, slope_intercept,
                      point_idx_on_line)


@njit
def assert_nb(truth_value, assert_err_msg=""):
    if not truth_value:
        print(assert_err_msg)
        raise Exception


@njit
def degree(gen_pattern):
    """Maximum number of 'OWN's in a sub-sequence of length = WIN_LENGTH,
    full of OWN/EMPTY sqs."""

    n = len(gen_pattern)
    max_owns = 0
    for i in range(n - WIN_LENGTH + 1):
        owns = 0
        for j in range(WIN_LENGTH):
            if gen_pattern[i + j] not in (OWN, EMPTY):
                break

            if gen_pattern[i + j] == OWN:
                owns += 1
        else:
            max_owns = max(max_owns, owns)

    return max_owns


@njit
def defcon_from_degree(d):
    return MAX_DEFCON - d


@njit
def is_one_step_from_straight_threat(gen_pattern):
    """True if a straight threat (straight four) can be
    achieved in one move."""

    n = len(gen_pattern)

    # Length of a straight threat: WIN_LENGTH - 1 OWN's in a row,
    # with an empty space on either side.
    l = WIN_LENGTH + 1

    for idx, v in enumerate(gen_pattern):
        if v == EMPTY:
            for i in range(n - l + 1):
                for j in range(l):
                    # Straight threat pattern value.
                    value = EMPTY if j in (0, l - 1) else OWN

                    if i + j == idx:
                        if value != OWN:
                            break
                    else:
                        if value != gen_pattern[i + j]:
                            break
                else:
                    return True

    return False


def new_threat_seq_item(next_sq, critical_sqs=None):
    item = {"next_sq": next_sq,
            "critical_sqs": critical_sqs}

    return item


@unique
class MoveType(IntEnum):
    EMPTY = auto()
    POINT = auto()
    COMBINATION = auto()


def new_move(threat_seqs=[]):
    next_sqs = None
    critical_sqs = None
    last_sqs = []
    move_type = MoveType.EMPTY

    if not threat_seqs:
        pass
    elif len(threat_seqs) == 1:
        assert len(threat_seqs[0]) == 1
        next_sqs = set([threat_seqs[0][0]["next_sq"]])
        critical_sqs = threat_seqs[0][0]["critical_sqs"]
        last_sqs.append(threat_seqs[0][0]["next_sq"])
        move_type = MoveType.POINT
    else:
        next_sqs = set()
        critical_sqs = set()
        for threat_seq in threat_seqs:
            seq_len = len(threat_seq)
            assert seq_len > 0
            for i, item in enumerate(threat_seq):
                assert item["next_sq"] not in next_sqs
                next_sqs.add(item["next_sq"])

                assert not critical_sqs.intersection(item["critical_sqs"])
                critical_sqs.update(item["critical_sqs"])

                if i == seq_len - 1:
                    last_sqs.append(item["next_sq"])

        move_type = MoveType.COMBINATION

    if next_sqs is not None and critical_sqs is not None:
        assert not set.intersection(next_sqs, critical_sqs)

    move = {"threat_seqs": threat_seqs,
            "next_sqs": next_sqs,
            "critical_sqs": critical_sqs,
            "last_sqs": last_sqs,
            "move_type": move_type}

    return move


def new_search_node(move, threats=[], potential_win=False, children=[]):
    node = {"move": move,
            "threats": threats,
            "potential_win": potential_win,
            "children": children}

    return node


def get_threat_sequence(node, path):
    sequence = []

    sub_node = node
    for seq in sub_node["move"]["threat_seqs"]:
        sequence.extend(seq)

    for idx in path:
        sub_node = sub_node["children"][idx]
        for seq in sub_node["move"]["threat_seqs"]:
            sequence.extend(seq)

    return sequence


def next_sqs_info_from_node(node, path=[], cumulative_nsqs=set(),
                            cumulative_csqs=set()):
    next_sqs_info = []

    next_sqs = (node["move"]["next_sqs"]
                if node["move"]["next_sqs"] is not None
                else set())
    critical_sqs = (node["move"]["critical_sqs"]
                    if node["move"]["critical_sqs"] is not None
                    else set())

    cumulative_nsqs_new = set.union(cumulative_nsqs, next_sqs)
    cumulative_csqs_new = set.union(cumulative_csqs, critical_sqs)

    if node["move"]["last_sqs"]:
        next_sqs_info.append({"next_sq": node["move"]["last_sqs"][-1],
                              "path": path.copy(),
                              "cumulative_nsqs": cumulative_nsqs_new,
                              "cumulative_csqs": cumulative_csqs_new})

    for i, child in enumerate(node["children"]):
        next_sqs_info.extend(next_sqs_info_from_node(child,
                                                     path + [i],
                                                     cumulative_nsqs_new,
                                                     cumulative_csqs_new))

    return next_sqs_info


def dedupe_line_items(items):
    i = 0
    n = len(items)

    while i < n - 1:
        val = items[i]
        j = i + 1

        while j < n:
            if items[j][1] == val[1] and items[j][0]["path"] == val[0]["path"]:
                del items[j]
                n -= 1
            else:
                j += 1

        i += 1


def lines_from_next_sqs_info_arr(next_sqs_info_arr):
    next_sqs_info_all = [(y, i) for (i, x) in enumerate(next_sqs_info_arr)
                         for y in x]
    n = len(next_sqs_info_all)

    lines_dict = dict()
    for i in range(n):
        item_i = next_sqs_info_all[i]
        val_i = item_i[0]
        idx_i = item_i[1]
        nsq_i = val_i["next_sq"]
        c_nsqs_i = val_i["cumulative_nsqs"]
        c_csqs_i = val_i["cumulative_csqs"]

        for j in range(i + 1, n):
            item_j = next_sqs_info_all[j]
            val_j = item_j[0]
            idx_j = item_j[1]
            nsq_j = val_j["next_sq"]
            c_nsqs_j = val_j["cumulative_nsqs"]
            c_csqs_j = val_j["cumulative_csqs"]

            # NOTE: Same gain_sq case is being excluded.
            #       It does not need to be handled.
            if (is_normal_line(nsq_i, nsq_j)
                and chebyshev_distance(nsq_i, nsq_j) < MAX_DEFCON
                and idx_i != idx_j
                and not set.intersection(c_nsqs_i, c_csqs_j)
                and not set.intersection(c_csqs_i, c_nsqs_j)
                and not set.intersection(c_csqs_i, c_csqs_j)):

                line = slope_intercept(nsq_i, nsq_j)

                if line in lines_dict:
                    lines_dict[line].append(item_i)
                    lines_dict[line].append(item_j)
                else:
                    lines_dict[line] = [item_i, item_j]

    for v in lines_dict.values():
        dedupe_line_items(v)

    return lines_dict


def point_set_is_useful(point_set, line):
    # Check that the points in the combination are close enough.
    point_idxs = [point_idx_on_line(x[0]["next_sq"], line) for x in point_set]
    point_set_range = max(point_idxs) - min(point_idxs)
    if MAX_DEFCON <= point_set_range:
        return False

    # Check that the point trees are not in conflict.
    n = len(point_set)

    for i in range(n):
        item_i = point_set[i]
        val_i = item_i[0]
        idx_i = item_i[1]
        c_nsqs_i = val_i["cumulative_nsqs"]
        c_csqs_i = val_i["cumulative_csqs"]

        for j in range(i + 1, n):
            item_j = point_set[j]
            val_j = item_j[0]
            idx_j = item_j[1]
            c_nsqs_j = val_j["cumulative_nsqs"]
            c_csqs_j = val_j["cumulative_csqs"]

            if not (idx_i != idx_j
                    and not set.intersection(c_nsqs_i, c_csqs_j)
                    and not set.intersection(c_csqs_i, c_nsqs_j)
                    and not set.intersection(c_csqs_i, c_csqs_j)):
                return False

    return True
