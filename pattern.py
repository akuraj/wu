import numpy as np
from consts import (GEN_ELEMS, EMPTY, DEFCON_RANGE, OWN, WALL_ENEMY, NOT_OWN)


class Pattern:
    """Pattern: Used to represent generic patterns (including threat patterns)."""

    def __init__(self,
                 pattern,
                 critical_sqs,
                 defcon):

        # Make sure pattern has valid elements.
        for elem in pattern:
            assert elem in GEN_ELEMS

        # Checks on critical_sqs
        critical_sqs.sort()
        critical_sqs_uniq = list(set(critical_sqs))
        critical_sqs_uniq.sort()
        assert critical_sqs == critical_sqs_uniq
        allowed = range(len(pattern))
        for sq in critical_sqs:
            # sq must be EMPTY for it to be critical.
            assert sq in allowed and pattern[sq] == EMPTY

        # Check on defcon.
        assert defcon in DEFCON_RANGE

        self.pattern = np.array(pattern, dtype=np.byte)
        self.critical_sqs = np.array(critical_sqs, dtype=np.byte)
        self.own_sqs = np.array([i for i, v in enumerate(pattern) if v == OWN], dtype=np.byte)
        self.defcon = defcon


# Win pattern.
P_WIN = Pattern([OWN, OWN, OWN, OWN, OWN], [], 0)

# Threat patterns.
P_4_ST = Pattern([EMPTY, OWN, OWN, OWN, OWN, EMPTY], [0, 5], 1)
P_4_A = Pattern([WALL_ENEMY, OWN, OWN, OWN, OWN, EMPTY], [5], 1)
P_4_B = Pattern([NOT_OWN, OWN, OWN, OWN, EMPTY, OWN], [4], 1)
P_4_C = Pattern([NOT_OWN, OWN, OWN, EMPTY, OWN, OWN, NOT_OWN], [3], 1)
P_3_ST = Pattern([EMPTY, EMPTY, OWN, OWN, OWN, EMPTY, EMPTY], [1, 5], 2)
P_3_A = Pattern([WALL_ENEMY, EMPTY, OWN, OWN, OWN, EMPTY, EMPTY], [1, 5, 6], 2)
P_3_B = Pattern([EMPTY, OWN, OWN, EMPTY, OWN, EMPTY], [0, 3, 5], 2)
