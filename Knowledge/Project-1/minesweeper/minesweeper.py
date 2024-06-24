import itertools
import random
import copy


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # Mark the cell as safe and update sentences that contain the cell
        self.mark_safe(cell)

        # Add a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        neighbors = self.get_cell_neighbors(cell)
        for cell in tuple(neighbors):
            if cell in self.mines:
                count -= 1
                neighbors.remove(cell)
            elif cell in self.safes:
                neighbors.remove(cell)

        # Construct sentence
        sentence = Sentence(neighbors, count)
        self.knowledge.append(sentence)

        # Mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        if sentence.known_safes():
            for cell in tuple(sentence.known_safes()):
                self.mark_safe(cell)

        if sentence.known_mines():
            for cell in tuple(sentence.known_mines()):
                self.mark_mine(cell)

        # Construct any new sentences if they can be inferred from existing knowledge
        sentences_to_add = []
        if len(self.knowledge) >= 2:
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    if (
                        not (sentence1 == sentence2)
                        and not (len(sentence1.cells) == 0)
                        and not (len(sentence2.cells) == 0)
                        and sentence1.cells.issubset(sentence2.cells)
                    ):
                        difference = sentence2.cells.difference(sentence1.cells)
                        sentences_to_add.append(
                            Sentence(difference, sentence2.count - sentence1.count)
                        )

        # Add newly inferred sentences to the knowledge base
        for sentence in sentences_to_add:
            if not sentence in self.knowledge:
                print(f"Adding inferred sentence: {sentence}")
                self.knowledge.append(sentence)

        # Go back through the knowledge base and mark known safes and mines based on newly inferred info
        for sentence in self.knowledge:
            if sentence.known_safes():
                for cell in tuple(sentence.known_safes()):
                    self.mark_safe(cell)

            if sentence.known_mines():
                for cell in tuple(sentence.known_mines()):
                    self.mark_mine(cell)

    def get_cell_neighbors(self, cell):
        neighbors = set()
        cell_i, cell_j = cell
        for i in range(cell_i - 1, cell_i + 2):
            for j in range(cell_j - 1, cell_j + 2):
                if 0 <= i < self.height and 0 <= j < self.width and not cell == (i, j):
                    neighbors.add((i, j))

        return neighbors

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_copy = copy.deepcopy(self.safes)

        while not len(safe_copy) == 0:
            possible_move = safe_copy.pop()
            if not possible_move in self.moves_made:
                return possible_move

        # No safe moves that have not already been made
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        potential_moves = set()

        # Populate potential_moves with a full board, except for moves already made and moves known to be mines
        for i in range(self.width):
            for j in range(self.height):
                move = (i, j)
                if not move in self.mines and not move in self.moves_made:
                    potential_moves.add(move)

        # Randomly pick from potential moves
        return random.choice(tuple(potential_moves))
