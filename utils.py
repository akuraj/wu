from enum import IntEnum, auto, unique
from numba import njit


@njit
def assert_nb(truth_value, assert_err_msg=""):
    if not truth_value:
        print(assert_err_msg)
        raise Exception


def new_threat_seq_item(next_sq, critical_sqs=None):
    item = {"next_sq": next_sq,
            "critical_sqs": critical_sqs}

    return item


@unique
class MoveType(IntEnum):
    NONE = auto()
    POINT = auto()


def new_move(threat_seqs=[]):
    next_sqs = None
    critical_sqs = None
    last_sqs = []
    move_type = MoveType.NONE

    if not threat_seqs:
        pass
    elif len(threat_seqs) == 1:
        assert len(threat_seqs[0]) == 1
        next_sqs = set([threat_seqs[0][0]["next_sq"]])
        critical_sqs = threat_seqs[0][0]["critical_sqs"]
        last_sqs.append(threat_seqs[0][0]["next_sq"])
        move_type = MoveType.POINT
    else:
        raise Exception

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


def next_sqs_from_threat_seqs(threat_seqs):
    return [x["next_sq"] for seq in threat_seqs for x in seq]


def potential_win_variations(node):
    variations = []

    if node["potential_win"]:
        node_var = next_sqs_from_threat_seqs(node["move"]["threat_seqs"])

        if node["children"]:
            for child in node["children"]:
                if child["potential_win"]:
                    child_variations = potential_win_variations(child)
                    for child_variation in child_variations:
                        variations.append(node_var + child_variation)
        else:
            variations.append(node_var)

    return variations
