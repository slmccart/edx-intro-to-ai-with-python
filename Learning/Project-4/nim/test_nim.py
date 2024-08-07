from nim import NimAI


def test_get_q_value():
    nimAI = NimAI()
    nimAI.q = {((1, 3, 5, 7), (1, 1)): 1.0, ((1, 3, 5, 7), (1, 2)): -1.0}

    assert nimAI.get_q_value([1, 3, 5, 7], (1, 2)) == -1.0
    assert nimAI.get_q_value([1, 3, 5, 7], (1, 3)) == 0


def test_update_q_value():
    nimAI = NimAI()
    nimAI.q = {((1, 3, 5, 7), (1, 1)): 1.0, ((1, 3, 5, 7), (1, 2)): -1.0}

    assert nimAI.get_q_value([1, 3, 5, 7], (1, 2)) == -1.0
    nimAI.update_q_value([1, 3, 5, 7], (1, 2), -1.0, 0, 1)
    assert nimAI.get_q_value([1, 3, 5, 7], (1, 2)) == 0

    assert nimAI.get_q_value([1, 3, 5, 7], (1, 1)) == 1.0
    nimAI.update_q_value([1, 3, 5, 7], (1, 1), 1.0, 0, -1)
    assert nimAI.get_q_value([1, 3, 5, 7], (1, 1)) == 0


def test_best_future_reward_no_possible_actions():
    nimAI = NimAI()

    assert nimAI.best_future_reward([0, 0, 0, 0]) == 0


def test_best_future_reward():
    nimAI = NimAI()
    nimAI.q = {
        ((1, 3, 5, 7), (1, 1)): 1.0,
        ((1, 3, 5, 7), (1, 2)): -1.0,
        ((1, 3, 5, 7), (0, 1)): 0,
    }

    assert nimAI.best_future_reward([1, 3, 5, 7]) == 1


def test_choose_action():
    nimAI = NimAI()
    nimAI.q = {
        ((1, 3, 5, 7), (1, 1)): 1.0,
        ((1, 3, 5, 7), (1, 2)): -1.0,
        ((1, 3, 5, 7), (0, 1)): 0,
    }

    assert nimAI.choose_action([1, 3, 5, 7], False) == (1, 1)


def test_choose_action_one_option():
    nimAI = NimAI()

    assert nimAI.choose_action([1, 0, 0, 0], False) == (0, 1)


if __name__ == "__main__":
    test_best_future_reward()
