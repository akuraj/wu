def test_truth():
    truth = True
    beauty = True

    assert False

    if truth == beauty:
        print("Truth = Beauty!")
    else:
        raise Exception("How can this be?!")
