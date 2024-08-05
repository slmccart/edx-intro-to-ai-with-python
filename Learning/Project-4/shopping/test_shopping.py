from shopping import load_data


def test_load_data():
    evidence, labels = load_data("test_shopping.csv")

    assert len(evidence) == 4
    assert len(evidence[0]) == 17
    assert evidence[0] == [0, 0, 0, 0, 1, 0, 0.2, 0.2, 0, 0, 1, 1, 1, 1, 1, 1, 0]
    assert evidence[3] == [
        0,
        0,
        0,
        0,
        2,
        2.666666667,
        0.05,
        0.14,
        0,
        0,
        11,
        3,
        2,
        2,
        4,
        0,
        1,
    ]
    assert len(labels) == 4
    assert labels == [1, 0, 0, 0]


if __name__ == "__main__":
    test_load_data()
