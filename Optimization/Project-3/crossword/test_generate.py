from generate import CrosswordCreator
from crossword import Crossword


def test_enforce_node_consistency():
    cc = CrosswordCreator(Crossword("data/structure0.txt", "data/words0.txt"))

    cc.enforce_node_consistency()

    for domain in cc.domains:
        for word in cc.domains[domain]:
            assert len(word) == domain.length


if __name__ == "__main__":
    test_enforce_node_consistency()
