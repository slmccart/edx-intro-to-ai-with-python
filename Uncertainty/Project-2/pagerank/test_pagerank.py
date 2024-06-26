from pagerank import transition_model
from pagerank import sample_pagerank
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


def test_sample_pagerank():
    ranks = sample_pagerank(
        corpus={
            "1.html": {"2.html", "3.html"},
            "2.html": {"3.html"},
            "3.html": {"2.html"},
        },
        damping_factor=0.85,
        n=1000,
    )

    assert len(ranks) == 3

    sum = 0
    for page in ranks:
        print(f"Page: {page}, Rank: {ranks[page]}")
        sum += ranks[page]
    assert sum == approx(1)


if __name__ == "__main__":
    test_sample_pagerank()
