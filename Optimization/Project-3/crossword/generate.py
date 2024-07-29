import sys

from crossword import *
from collections import deque


class CrosswordCreator:

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Loop over each variable (set of blank spaces)
        for variable in self.domains:
            # Loop over a copy of the domain for each variable, since we cannot modify
            #   the set we are looping over
            for word in self.domains[variable].copy():
                # If a word in the domain does not match the length of the variable,
                #   remove the word from the domain
                if len(word) != variable.length:
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        return_val = False
        # If no overlap between variables, then nothing to do
        if y not in self.crossword.neighbors(x):
            return False

        # Get position of overlap for each variable
        x_pos, y_pos = self.crossword.overlaps[(x, y)]

        # Loop over copy of x domain (copy is necessary since x domain may be modified)
        for x_word in self.domains[x].copy():
            found_possible_word = False
            # Loop over all words in y domain
            for y_word in self.domains[y]:
                # Check if the letters in the overlap position match
                if x_word[x_pos] == y_word[y_pos]:
                    found_possible_word = True
                    break

            # If no matches in the overlap position were found for this word, then remove it from x domain
            if not found_possible_word:
                self.domains[x].remove(x_word)
                return_val = True

        return return_val

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # If arcs was not passed in, initialize queue with all of the overlapping variables
        #   in the crossword
        if arcs == None:
            arcs = deque(
                [k for k, v in self.crossword.overlaps.items() if v is not None]
            )
        # Else, convert the incoming list to a queue
        else:
            arcs = deque(arcs)

        # While arcs is not empty
        while arcs:
            # Pop first pair of variables from queue
            x, y = arcs.popleft()

            # Make the arc arc-consistent
            if self.revise(x, y):
                # If the domain of x is empty, return False since this can't be a solution
                if len(self.domains[x]) == 0:
                    return False

                # Since the domain of x changed, we need to add arcs for all of x's neighbors to the queue
                for z in self.crossword.neighbors(x) - {y}:
                    arcs.append((z, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        for var in self.crossword.variables:
            if var not in assignment:
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check that the assignment contains no duplicate entries
        if len(assignment.values()) != len(set(assignment.values())):
            return False

        # Check that all assignments are consistent with the length of their variable
        # NOTE: This needs to be done for all assignments before considering neighbors, since an
        #       assignment that is not long enough could cause an indexing error when checking
        #       overlapped assignments
        for x, x_word in assignment.items():
            if len(x_word) != x.length:
                return False

        # Check that all assignments satisfy binary constraints
        for x, x_word in assignment.items():
            for neighbor in self.crossword.neighbors(x):
                if neighbor in assignment:
                    pos_x, pos_neighbor = self.crossword.overlaps[(x, neighbor)]
                    if assignment[x][pos_x] != assignment[neighbor][pos_neighbor]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        vals = self.domains[var]

        # Initialize dictionary of domain values and a count of how many values
        #   they rule out in neighboring variables' domains
        domain_values = {}
        for val in vals:
            domain_values[val] = 0

        # Loop through var's unassigned neighbors
        for neighbor in self.crossword.neighbors(var) - assignment.keys():
            # Grab overlapping position of var and neighbor
            var_pos, neighbor_pos = self.crossword.overlaps[(var, neighbor)]

            # For every val in var's domain track how many neighbor values would be eliminated
            #   if val were assigned
            for val in vals:
                # If val is in a neighbor's domain, add an elimination
                if val in self.domains[neighbor]:
                    domain_values[val] += 1

                # For every val in neighbor's domain count eliminations from mismatched characters
                #   at the overlap
                for neighbor_val in self.domains[neighbor]:
                    if val[var_pos] != neighbor_val[neighbor_pos]:
                        domain_values[val] += 1

        return sorted(domain_values, key=domain_values.get)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Get all variables that have not been assigned
        remaining = self.crossword.variables - assignment.keys()

        # If only one variable is remaining, then return it
        if len(remaining) == 1:
            return remaining.pop()

        # Find the variable with the fewest remaining values in its domain
        #   Use a dictionary with number of remaining values as a key and build a list of variables as the value
        #   Using a list of variables as the value will let us handle ties later
        min_remaining_values = {}
        for var in remaining:
            n = len(self.domains[var])
            if n in min_remaining_values:
                min_remaining_values[n] += [var]
            else:
                min_remaining_values[n] = [var]

        # Sort min_remaining_values by key (values remaining)
        sorted_min_remaining_values = {
            key: min_remaining_values[key] for key in sorted(min_remaining_values)
        }

        # Get the first value in the sorted dictionary
        min_remaining_variables = sorted_min_remaining_values[
            next(iter(sorted_min_remaining_values))
        ]

        # If there was not a tie for the lowest number of remaining values, then return the variable
        if len(min_remaining_variables) == 1:
            return min_remaining_variables.pop()

        # Initialize tracking for variable with the most neighbors
        max_neighbors = 0
        most_neighors = None

        # Find variable with the most neighbors
        for var in min_remaining_variables:
            num_neighbors = len(self.crossword.neighbors(var))
            if num_neighbors > max_neighbors:
                max_neighbors = num_neighbors
                most_neighors = var

        return most_neighors

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # If assignment is complete, then the search is complete and we can return assignment
        if self.assignment_complete(assignment):
            return assignment

        # Get the next unassigned variable
        var = self.select_unassigned_variable(assignment)

        # Try to assign values in order of preference
        for value in self.order_domain_values(var, assignment):
            # If the assignment is consistent
            if self.consistent(assignment):
                # Add the variable-value mapping to assignment
                assignment[var] = value
                # Continue the backtracking search with the new assignment
                result = self.backtrack(assignment)
                # If that assignment was good, then return the result
                if result != None:
                    return result

                # If the assignment was not good, then remove that variable-value mapping and
                #   continue with the next value
                assignment.pop(var, None)

            # If we tried all values and were not successful, then return None
            return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
