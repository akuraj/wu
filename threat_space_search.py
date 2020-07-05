"""Implements Threat Space Search."""

from time import sleep
from functools import reduce
from consts import STONE, MAX_DEFCON, ANIMATION_TIMESTEP
from board import set_sq, clear_sq, board_to_str
from pattern import (ThreatPri, search_all_board, search_all_point_own,
                     search_all_board_get_next_sqs,
                     search_all_point_own_get_next_sqs, search_all_point)
from geometry import point_is_on_line


def new_search_node(next_sq, critical_sqs, win, children):
    return {"next_sq": next_sq,
            "critical_sqs": critical_sqs,
            "win": win,
            "children": children}


def tss_next_sq(board, color, next_sq, all_threats_init, opp_all_threats_init):
    """Threat Space Search for a given next_sq."""

    set_sq(board, color, next_sq)

    # Create all_threats for self and opponent, and update them.
    # 1. Remove threats including next_sq.
    # 2. Compute new threats including next_sq.
    all_threats = [x for x in all_threats_init
                   if not point_is_on_line(next_sq,
                                           x["match"][0],
                                           x["match"][1],
                                           True)]
    all_threats.extend(search_all_point(board,
                                        color,
                                        next_sq,
                                        ThreatPri.IMMEDIATE))

    opp_all_threats = [x for x in opp_all_threats_init
                       if not point_is_on_line(next_sq,
                                               x["match"][0],
                                               x["match"][1],
                                               True)]
    opp_all_threats.extend(search_all_point(board,
                                            color ^ STONE,
                                            next_sq,
                                            ThreatPri.IMMEDIATE))

    # NOTE: If we are potentially losing, we will early return.

    # Check if we are potentially losing, by looking at the updated lists of all threats.
    min_defcon = reduce(min, [x["defcon"] for x in all_threats], MAX_DEFCON)
    opp_min_defcon = reduce(min, [x["defcon"] for x in opp_all_threats], MAX_DEFCON)

    potential_loss = len(opp_all_threats) > 0 and opp_min_defcon <= min_defcon
    if potential_loss:
        clear_sq(board, color, next_sq)

        return new_search_node(next_sq, set(), False, [])

    threats = search_all_point_own(board, color, next_sq, ThreatPri.IMMEDIATE)

    # We will consider those of our threats which are more immediate
    # than all of our opponent's threats.
    pressing_threats = [x for x in threats if x["defcon"] < opp_min_defcon]

    critical_sqs = (reduce(set.intersection, [x["critical_sqs"] for x in pressing_threats])
                    if pressing_threats
                    else set())

    for csq in critical_sqs:
        set_sq(board, color ^ STONE, csq)

    # If we have any critical_sqs, update lists of all threats.
    # Also check if we are potentially losing after the critical_sqs are covered by the opponent.
    if critical_sqs:
        all_threats = [x for x in all_threats
                       if not any([point_is_on_line(p,
                                                    x["match"][0],
                                                    x["match"][1],
                                                    True)
                                   for p in critical_sqs])]

        opp_all_threats = [x for x in opp_all_threats
                           if not any([point_is_on_line(p,
                                                        x["match"][0],
                                                        x["match"][1],
                                                        True)
                                       for p in critical_sqs])]

        for csq in critical_sqs:
            all_threats.extend(search_all_point(board, color, csq, ThreatPri.IMMEDIATE))
            opp_all_threats.extend(search_all_point(board,
                                                    color ^ STONE,
                                                    csq,
                                                    ThreatPri.IMMEDIATE))

        min_defcon = reduce(min, [x["defcon"] for x in all_threats], MAX_DEFCON)
        opp_min_defcon = reduce(min, [x["defcon"] for x in opp_all_threats], MAX_DEFCON)

        # If opp_min_defcon is 0, then the opponent has potentially won!
        potential_loss = opp_min_defcon == 0
        if potential_loss:
            for csq in critical_sqs:
                clear_sq(board, color ^ STONE, csq)

            clear_sq(board, color, next_sq)

            return new_search_node(next_sq, set(), False, [])

        # We will consider those of the opponent's threats
        # which are more immediate than all of our threats.
        opp_pressing_threats = [x for x in opp_all_threats
                                if x["defcon"] < min_defcon]
        opp_critical_sqs = (reduce(set.intersection,
                                   [x["critical_sqs"] for x in opp_pressing_threats])
                            if opp_pressing_threats
                            else set())

        potential_loss = len(opp_pressing_threats) > 0 and len(opp_critical_sqs) == 0
        if potential_loss:
            for csq in critical_sqs:
                clear_sq(board, color ^ STONE, csq)

            clear_sq(board, color, next_sq)

            return new_search_node(next_sq, set(), False, [])

    win = len(pressing_threats) > 0 and len(critical_sqs) == 0
    children = []

    # If next_sq produces no threats or we've found a potential win, we stop.
    if len(threats) > 0 and not win:
        children = [tss_next_sq(board, color, x, all_threats, opp_all_threats)
                    for x in search_all_point_own_get_next_sqs(board,
                                                               color,
                                                               next_sq,
                                                               ThreatPri.IMMEDIATE)]
        win = any([x["win"] for x in children])

        if not win:
            children_other = [tss_next_sq(board, color, x, all_threats, opp_all_threats)
                              for x in search_all_point_own_get_next_sqs(board,
                                                                         color,
                                                                         next_sq,
                                                                         ThreatPri.NON_IMMEDIATE)]
            win = any([x["win"] for x in children_other])
            children.extend(children_other)

    for csq in critical_sqs:
        clear_sq(board, color ^ STONE, csq)

    clear_sq(board, color, next_sq)

    return new_search_node(next_sq, critical_sqs, win, children)


def tss_board(board, color):
    """Threat Space Search for the whole board."""

    threats = search_all_board(board, color, ThreatPri.IMMEDIATE)
    opp_threats = search_all_board(board, color ^ STONE, ThreatPri.IMMEDIATE)

    min_defcon = reduce(min, [x["defcon"] for x in threats], MAX_DEFCON)
    opp_min_defcon = reduce(min, [x["defcon"] for x in opp_threats], MAX_DEFCON)

    win = len(threats) > 0 and min_defcon <= opp_min_defcon
    children = []

    if not win:
        children = [tss_next_sq(board, color, x, threats, opp_threats)
                    for x in search_all_board_get_next_sqs(board, color,
                                                           ThreatPri.IMMEDIATE)]
        win = any([x["win"] for x in children])

    return new_search_node(None, None, win, children)


def win_variations(node):
    variations = []

    if node["win"]:
        node_var = [(node["next_sq"], node["critical_sqs"])] if node["next_sq"] is not None else []

        if node["children"]:
            for child in node["children"]:
                if child["win"]:
                    child_variations = win_variations(child)
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
        print(board_to_str(board))
        sleep(ANIMATION_TIMESTEP)

        for csq in item[1]:
            set_sq(board, color ^ STONE, csq)

        if item[1]:
            print(board_to_str(board))
            sleep(ANIMATION_TIMESTEP)

    for item in variation:
        clear_sq(board, color, item[0])

        for csq in item[1]:
            clear_sq(board, color ^ STONE, csq)
