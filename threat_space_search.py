"""Implements Threat Space Search."""

from time import sleep
from functools import reduce
from consts import STONE
from board import set_sq, clear_sq, board_to_str
from pattern import (ThreatPri, search_all_board, search_all_point_own,
                     search_all_board_get_next_sqs,
                     search_all_point_own_get_next_sqs)

ANIMATION_TIMESTEP = 2


def new_search_node(next_sq, threats, critical_sqs, potential_win, children):
    # # Only keep potentially winning children.
    # children = [x for x in children if x["potential_win"]]

    node = {"next_sq": next_sq,
            "threats": threats,
            "critical_sqs": critical_sqs,
            "potential_win": potential_win,
            "children": children}

    return node


def tss_next_sq(board, color, next_sq):
    """Threat Space Search for a given next_sq."""

    set_sq(board, color, next_sq)

    threats = search_all_point_own(board, color, next_sq, ThreatPri.IMMEDIATE)
    critical_sqs = (reduce(set.intersection, [x["critical_sqs"] for x in threats])
                    if threats
                    else set())
    potential_win = len(threats) > 0 and len(critical_sqs) == 0
    children = []

    # If the opponent is potentially winning by playing at one of the critical_sqs,
    # then this variation is assumed to not be winning.
    for csq in critical_sqs:
        set_sq(board, color ^ STONE, csq)

        threats_csq = search_all_point_own(board, color ^ STONE,
                                           csq, ThreatPri.IMMEDIATE)
        critical_sqs_csq = (reduce(set.intersection, [x["critical_sqs"] for x in threats_csq])
                            if threats_csq
                            else set())
        potential_win_csq = len(threats_csq) > 0 and len(critical_sqs_csq) == 0

        clear_sq(board, color ^ STONE, csq)

        if potential_win_csq:
            potential_win = False
            clear_sq(board, color, next_sq)
            return new_search_node(next_sq, threats, critical_sqs, potential_win, children)

    # If next_sq produces no threats or we've found a potential win, we stop.
    if len(threats) > 0 and not potential_win:
        for csq in critical_sqs:
            set_sq(board, color ^ STONE, csq)

        children = [tss_next_sq(board, color, x)
                    for x in search_all_point_own_get_next_sqs(board,
                                                               color,
                                                               next_sq,
                                                               ThreatPri.IMMEDIATE)]
        potential_win = any([x["potential_win"] for x in children])

        if not potential_win:
            children_other = [tss_next_sq(board, color, x)
                              for x in search_all_point_own_get_next_sqs(board,
                                                                         color,
                                                                         next_sq,
                                                                         ThreatPri.NON_IMMEDIATE)]
            potential_win = any([x["potential_win"] for x in children_other])
            children.extend(children_other)

        for csq in critical_sqs:
            clear_sq(board, color ^ STONE, csq)

    clear_sq(board, color, next_sq)

    return new_search_node(next_sq, threats, critical_sqs, potential_win, children)


def tss_board(board, color):
    """Threat Space Search for the whole board."""

    threats = search_all_board(board, color, ThreatPri.IMMEDIATE)
    potential_win = len(threats) > 0
    children = []

    if not potential_win:
        children = [tss_next_sq(board, color, x)
                    for x in search_all_board_get_next_sqs(board, color,
                                                           ThreatPri.IMMEDIATE)]
        potential_win = any([x["potential_win"] for x in children])

    return new_search_node(None, threats, None, potential_win, children)


def potential_win_variations(node):
    variations = []

    if node["potential_win"]:
        node_var = [(node["next_sq"], node["critical_sqs"])] if node["next_sq"] is not None else []

        if node["children"]:
            for child in node["children"]:
                if child["potential_win"]:
                    child_variations = potential_win_variations(child)
                    for child_var in child_variations:
                        variations.append(node_var + child_var)
        else:
            variations.append(node_var)

    return variations


def animate_variation(board, color, variation):
    print(board_to_str(board))
    sleep(ANIMATION_TIMESTEP)

    for item in variation:
        set_sq(board, color, item[0])

        for csq in item[1]:
            set_sq(board, color ^ STONE, csq)

        print(board_to_str(board))
        sleep(ANIMATION_TIMESTEP)

    for item in variation:
        clear_sq(board, color, item[0])

        for csq in item[1]:
            clear_sq(board, color ^ STONE, csq)
