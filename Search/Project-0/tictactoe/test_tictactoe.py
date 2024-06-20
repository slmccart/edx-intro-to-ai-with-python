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
    assert tictactoe.utility(full_board_tie) == 0
    assert (
        tictactoe.utility(
            [
                [X, X, X],
                [EMPTY, EMPTY, EMPTY],
                [O, O, O],
            ]
        )
        == 1
    )
    assert (
        tictactoe.utility(
            [
                [X, EMPTY, X],
                [EMPTY, X, EMPTY],
                [O, O, O],
            ]
        )
        == -1
    )


def test_terminal():
    assert tictactoe.terminal(tictactoe.initial_state()) == False
    assert tictactoe.terminal(full_board_tie) == True


def test_player():
    assert tictactoe.player(tictactoe.initial_state()) == X
    assert (
        tictactoe.player(
            [
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, X, EMPTY],
                [EMPTY, EMPTY, EMPTY],
            ]
        )
        == O
    )
    assert (
        tictactoe.player(
            [
                [EMPTY, EMPTY, O],
                [EMPTY, X, EMPTY],
                [EMPTY, EMPTY, EMPTY],
            ]
        )
        == X
    )
    # Doesn't matter the return value, but test that it doesn't blow up
    assert tictactoe.player(full_board_tie)


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
        [
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [X, O, X],
        ]
    )


def test_winner_full_rows():
    assert (
        tictactoe.winner(
            [
                [X, X, X],
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY],
            ]
        )
        == X
    )
    assert (
        tictactoe.winner(
            [
                [EMPTY, EMPTY, EMPTY],
                [O, O, O],
                [EMPTY, EMPTY, EMPTY],
            ]
        )
        == O
    )
    assert (
        tictactoe.winner(
            [
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY],
                [X, X, X],
            ]
        )
        == X
    )
    assert (
        tictactoe.winner(
            [
                [EMPTY, EMPTY, EMPTY],
                [EMPTY, EMPTY, EMPTY],
                [X, O, X],
            ]
        )
        == None
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


def test_winner_full_columns():
    assert (
        tictactoe.winner(
            [
                [X, EMPTY, EMPTY],
                [X, EMPTY, EMPTY],
                [X, EMPTY, EMPTY],
            ]
        )
        == X
    )
    assert (
        tictactoe.winner(
            [
                [EMPTY, O, EMPTY],
                [EMPTY, O, EMPTY],
                [EMPTY, O, EMPTY],
            ]
        )
        == O
    )
    assert (
        tictactoe.winner(
            [
                [EMPTY, EMPTY, X],
                [EMPTY, EMPTY, X],
                [EMPTY, EMPTY, X],
            ]
        )
        == X
    )
    assert (
        tictactoe.winner(
            [
                [EMPTY, EMPTY, O],
                [EMPTY, EMPTY, X],
                [EMPTY, EMPTY, O],
            ]
        )
        == None
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


def test_winner_full_diagonals():
    assert (
        tictactoe.winner(
            [
                [X, EMPTY, EMPTY],
                [EMPTY, X, EMPTY],
                [EMPTY, EMPTY, X],
            ]
        )
        == X
    )

    assert (
        tictactoe.winner(
            [
                [EMPTY, EMPTY, O],
                [EMPTY, O, EMPTY],
                [O, EMPTY, EMPTY],
            ]
        )
        == O
    )

    assert (
        tictactoe.winner(
            [
                [EMPTY, EMPTY, X],
                [EMPTY, X, EMPTY],
                [EMPTY, EMPTY, EMPTY],
            ]
        )
        == None
    )


def test_actions():
    assert tictactoe.actions(
        [
            [X, O, X],
            [X, O, X],
            [O, X, EMPTY],
        ]
    ) == {(2, 2)}

    assert tictactoe.actions(tictactoe.initial_state()) == {
        (0, 0),
        (0, 1),
        (0, 2),
        (1, 0),
        (1, 1),
        (1, 2),
        (2, 0),
        (2, 1),
        (2, 2),
    }

    assert tictactoe.actions(full_board_tie) == set()


# def main():
#     test_player()


# if __name__ == "__main__":
#     main()
