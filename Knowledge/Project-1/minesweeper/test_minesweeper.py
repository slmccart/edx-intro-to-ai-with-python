from minesweeper import Sentence


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
