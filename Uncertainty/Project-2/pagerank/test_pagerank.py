from pagerank import transition_model
from pytest import approx


def test_transition_model():
    model = transition_model(
        {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}},
        "1.html",
        0.85,
    )

    assert len(model) == 3

    sum = 0
    for page in model:
        sum += model[page]
    assert sum == 1

    assert model["1.html"] == approx(0.05)
    assert model["2.html"] == approx(0.475)
    assert model["3.html"] == approx(0.475)


def test_transition_model_no_outgoing_links():
    model = transition_model(
        {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {}},
        "3.html",
        0.85,
    )

    assert len(model) == 3

    sum = 0
    for page in model:
        sum += model[page]
    assert sum == 1

    assert model["1.html"] == 1 / 3
    assert model["2.html"] == 1 / 3
    assert model["3.html"] == 1 / 3


if __name__ == "__main__":
    test_transition_model()
