from numba import njit


@njit
def assert_nb(truth_value, assert_err_msg=""):
    """Raise an exception as opposed to using built-in assert.

    Asserts get caught in pytest, preventing us from njit-ting test functions.
    This function allows us to get around that.
    """

    if not truth_value:
        print(assert_err_msg)
        raise Exception
