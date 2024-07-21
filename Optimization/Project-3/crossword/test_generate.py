from generate import CrosswordCreator
from crossword import Crossword


def test_enforce_node_consistency():
    cc = CrosswordCreator(Crossword("data/structure0.txt", "data/words0.txt"))

    found_mismatch = False

    for domain in cc.domains:
        for word in cc.domains[domain]:
            if len(word) != domain.length:
                found_mismatch = True
                break

    assert found_mismatch

    cc.enforce_node_consistency()

    found_mismatch = False

    for domain in cc.domains:
        for word in cc.domains[domain]:
            if len(word) != domain.length:
                found_mismatch = True
                break

    assert not found_mismatch


if __name__ == "__main__":
    test_enforce_node_consistency()
