from generate import CrosswordCreator
from crossword import Crossword
from crossword import Variable


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


def test_revise():
    cc = CrosswordCreator(Crossword("data/structure0.txt", "data/words0.txt"))
    # Overlapping variables - cc.overlaps
    x = Variable(0, 1, Variable.DOWN, 5)
    y = Variable(0, 1, Variable.ACROSS, 3)

    # First enforce node consistency to narrow down domain to correct number of letters
    cc.enforce_node_consistency()

    # Assert domain before revision
    assert cc.domains[x] == {"SEVEN", "THREE", "EIGHT"}
    assert cc.domains[y] == {"ONE", "SIX", "TWO", "TEN"}

    # Revise x domain and assert domain was modified
    assert cc.revise(x, y)

    # Assert x domain after revision
    assert cc.domains[x] == {"THREE", "SEVEN"}
    # Assert y domain unchanged
    assert cc.domains[y] == {"ONE", "SIX", "TWO", "TEN"}


def test_revise_no_overlap():
    cc = CrosswordCreator(Crossword("data/structure0.txt", "data/words0.txt"))
    # Non-overlapping variables - cc.overlaps
    x = Variable(0, 1, Variable.DOWN, 5)
    y = Variable(1, 4, Variable.DOWN, 4)

    assert not cc.revise(x, y)


def test_ac3_no_list():
    cc = CrosswordCreator(Crossword("data/structure0.txt", "data/words0.txt"))
    cc.enforce_node_consistency()

    var1 = Variable(0, 1, Variable.DOWN, 5)
    var2 = Variable(4, 1, Variable.ACROSS, 4)
    var3 = Variable(0, 1, Variable.ACROSS, 3)
    var4 = Variable(1, 4, Variable.DOWN, 4)

    assert cc.domains[var1] == {"EIGHT", "THREE", "SEVEN"}
    assert cc.domains[var2] == {"NINE", "FIVE", "FOUR"}
    assert cc.domains[var3] == {"ONE", "TWO", "SIX", "TEN"}
    assert cc.domains[var4] == {"NINE", "FIVE", "FOUR"}

    assert cc.ac3()

    assert cc.domains[var1] == {"SEVEN"}
    assert cc.domains[var2] == {"NINE"}
    assert cc.domains[var3] == {"SIX"}
    assert cc.domains[var4] == {"NINE", "FIVE"}


def test_ac3_empty_arc_list():
    cc = CrosswordCreator(Crossword("data/structure0.txt", "data/words0.txt"))
    cc.enforce_node_consistency()

    assert cc.ac3([])


def test_ac3_initial_list():
    cc = CrosswordCreator(Crossword("data/structure0.txt", "data/words0.txt"))
    cc.enforce_node_consistency()

    var1 = Variable(0, 1, Variable.DOWN, 5)
    var2 = Variable(4, 1, Variable.ACROSS, 4)
    var3 = Variable(0, 1, Variable.ACROSS, 3)
    var4 = Variable(1, 4, Variable.DOWN, 4)

    assert cc.domains[var1] == {"EIGHT", "THREE", "SEVEN"}
    assert cc.domains[var2] == {"NINE", "FIVE", "FOUR"}
    assert cc.domains[var3] == {"ONE", "TWO", "SIX", "TEN"}
    assert cc.domains[var4] == {"NINE", "FIVE", "FOUR"}

    assert cc.ac3([(var1, var3)])

    assert cc.domains[var1] == {"SEVEN", "THREE"}
    assert cc.domains[var2] == {"NINE"}
    assert cc.domains[var3] == {"TEN", "ONE", "TWO", "SIX"}
    assert cc.domains[var4] == {"NINE", "FIVE"}


if __name__ == "__main__":
    # test_enforce_node_consistency()
    test_ac3_initial_list()
