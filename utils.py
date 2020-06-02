from numba import njit


@njit
def assert_nb(truth_value, assert_err_msg=""):
    if not truth_value:
        print(assert_err_msg)
        raise Exception


def new_search_node(next_sq, threats, critical_sqs, potential_win, children):
    node = {"next_sq": next_sq,
            "threats": threats,
            "critical_sqs": critical_sqs,
            "potential_win": potential_win,
            "children": children}

    return node


# TODO: Update the below func to new format!
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


def potential_win_variations(node):
    variations = []

    if node["potential_win"]:
        node_var = [node["next_sq"]] if node["next_sq"] is not None else []

        if node["children"]:
            for child in node["children"]:
                if child["potential_win"]:
                    child_variations = potential_win_variations(child)
                    for child_var in child_variations:
                        variations.append(node_var + child_var)
        else:
            variations.append(node_var)

    return variations
