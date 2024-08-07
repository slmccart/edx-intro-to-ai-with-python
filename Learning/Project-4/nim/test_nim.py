from nim import NimAI


def test_get_q_value():
    nimAI = NimAI()
    nimAI.q = {((1, 3, 5, 7), (1, 1)): 1.0, ((1, 3, 5, 7), (1, 2)): -1.0}

    assert nimAI.get_q_value([1, 3, 5, 7], (1, 2)) == -1.0
    assert nimAI.get_q_value([1, 3, 5, 7], (1, 3)) == 0


if __name__ == "__main__":
    test_get_q_value()
