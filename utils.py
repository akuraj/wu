from numba import njit


@njit
def assert_nb(truth_value, assert_err_msg=""):
    if not truth_value:
        print(assert_err_msg)
        raise Exception
