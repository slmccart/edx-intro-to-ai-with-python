from minesweeper import Sentence
from minesweeper import MinesweeperAI


def test_sentence_mark_mine():
    sentence = Sentence({(0, 0), (0, 1), (1, 0), (1, 1)}, 2)
    sentence.mark_mine((1, 1))
    assert sentence == Sentence({(0, 0), (0, 1), (1, 0)}, 1)

    sentence1 = Sentence({(0, 0), (0, 1), (1, 0), (1, 1)}, 2)
    sentence.mark_mine((3, 3))
    assert sentence1 == Sentence({(0, 0), (0, 1), (1, 0), (1, 1)}, 2)


def test_sentence_mark_safe():
    sentence = Sentence({(0, 0), (0, 1), (1, 0), (1, 1)}, 2)
    sentence.mark_safe((1, 1))
    assert sentence == Sentence({(0, 0), (0, 1), (1, 0)}, 2)

    sentence1 = Sentence({(0, 0), (0, 1), (1, 0), (1, 1)}, 2)
    sentence.mark_safe((3, 3))
    assert sentence1 == Sentence({(0, 0), (0, 1), (1, 0), (1, 1)}, 2)


def test_sentence_known_mines():
    sentence = Sentence({(0, 0), (0, 1), (1, 0), (1, 1)}, 4)
    assert sentence.known_mines() == {(0, 0), (0, 1), (1, 0), (1, 1)}

    sentence1 = Sentence({(0, 0), (0, 1), (1, 0), (1, 1)}, 2)
    assert sentence1.known_mines() == set()


def test_sentence_known_safes():
    sentence = Sentence({(0, 0), (0, 1), (1, 0), (1, 1)}, 0)
    assert sentence.known_safes() == {(0, 0), (0, 1), (1, 0), (1, 1)}

    sentence1 = Sentence({(0, 0), (0, 1), (1, 0), (1, 1)}, 2)
    assert sentence1.known_safes() == set()


def test_minesweeperai_make_safe_move():
    ai = MinesweeperAI(height=2, width=2)
    ai.safes = {(0, 0), (0, 1), (1, 0)}
    ai.moves_made = {(0, 0)}
    assert ai.make_safe_move() == (0, 1)

    ai1 = MinesweeperAI(height=2, width=2)
    ai1.safes = {(0, 0), (0, 1), (1, 0)}
    ai1.moves_made = {(0, 0), (0, 1), (1, 0)}
    assert ai1.make_safe_move() == None


def test_minesweeperai_make_random_move():
    ai = MinesweeperAI(height=2, width=2)
    ai.mines = {(0, 1)}
    ai.moves_made = {(0, 0)}
    assert ai.make_random_move() in {(1, 0), (1, 1)}


def test_minesweeperai_get_cell_neighbors():
    ai = MinesweeperAI(height=3, width=3)
    assert ai.get_cell_neighbors((1, 1)) == {
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2),
    }

    ai = MinesweeperAI(height=3, width=3)
    assert ai.get_cell_neighbors((0, 0)) == {(0, 1), (1, 0), (1, 1)}

    ai = MinesweeperAI(height=3, width=3)
    assert ai.get_cell_neighbors((2, 2)) == {(1, 1), (1, 2), (2, 1)}

    ai = MinesweeperAI(height=3, width=3)
    assert ai.get_cell_neighbors((1, 0)) == {(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)}

    ai = MinesweeperAI(height=4, width=5)
    assert ai.get_cell_neighbors((3, 4)) == {(2, 3), (2, 4), (3, 3)}


if __name__ == "__main__":
    test_minesweeperai_get_cell_neighbors()
