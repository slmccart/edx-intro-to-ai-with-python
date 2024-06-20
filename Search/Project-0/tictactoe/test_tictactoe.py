import tictactoe

X = "X"
O = "O"
EMPTY = None

full_board_tie = [
    [X, O, X],
    [O, X, O],
    [O, X, O],
]


def test_initial_state():
    assert tictactoe.initial_state() == [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
    ]


def test_utility():
    assert tictactoe.utility(tictactoe.initial_state()) == 0
    # assert tictactoe.utility(full_board_tie) == 0


def test_terminal():
    assert tictactoe.terminal(tictactoe.initial_state()) == False
    assert tictactoe.terminal(full_board_tie) == True


def test_terminal_full_rows():
    assert tictactoe.terminal(
        [
            [X, X, X],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
        ]
    )
    assert tictactoe.terminal(
        [
            [EMPTY, EMPTY, EMPTY],
            [O, O, O],
            [EMPTY, EMPTY, EMPTY],
        ]
    )
    assert tictactoe.terminal(
        [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [X, X, X],
        ]
    )
    assert not tictactoe.terminal(
        [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [X, O, X]]
    )


def test_terminal_full_columns():
    assert tictactoe.terminal(
        [
            [X, EMPTY, EMPTY],
            [X, EMPTY, EMPTY],
            [X, EMPTY, EMPTY],
        ]
    )
    assert tictactoe.terminal(
        [
            [EMPTY, X, EMPTY],
            [EMPTY, X, EMPTY],
            [EMPTY, X, EMPTY],
        ]
    )
    assert tictactoe.terminal(
        [
            [EMPTY, EMPTY, O],
            [EMPTY, EMPTY, O],
            [EMPTY, EMPTY, O],
        ]
    )
    assert not tictactoe.terminal(
        [
            [EMPTY, EMPTY, O],
            [EMPTY, EMPTY, X],
            [EMPTY, EMPTY, O],
        ]
    )


def test_terminal_full_diagonals():
    assert tictactoe.terminal(
        [
            [X, EMPTY, EMPTY],
            [EMPTY, X, EMPTY],
            [EMPTY, EMPTY, X],
        ]
    )

    assert tictactoe.terminal(
        [
            [EMPTY, EMPTY, X],
            [EMPTY, X, EMPTY],
            [X, EMPTY, EMPTY],
        ]
    )

    assert not tictactoe.terminal(
        [
            [EMPTY, EMPTY, X],
            [EMPTY, X, EMPTY],
            [EMPTY, EMPTY, EMPTY],
        ]
    )
