import copy
import itertools


class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

        # will count the number of times the backtracking function is called
        self.backtracking_call_counter = 0

        # will count the number of times the backtracking function returned failure
        self.backtracking_fail_counter = 0

    def add_variable(self, name, domain):
        """Add a new variable to the CSP. 'name' is the variable name
        and 'domain' is a list of the legal values for the variable.
        """
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def get_all_possible_pairs(self, a, b):
        """Get a list of all possible pairs (as tuples) of the values in
        the lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.
        """
        return itertools.product(a, b)

    def get_all_arcs(self):
        """Get a list of all arcs/constraints that have been defined in
        the CSP. The arcs/constraints are represented as tuples (i, j),
        indicating a constraint between variable 'i' and 'j'.
        """
        return [ (i, j) for i in self.constraints for j in self.constraints[i] ]

    def get_all_neighboring_arcs(self, var):
        """Get a list of all arcs/constraints going to/from variable
        'var'. The arcs/constraints are represented as in get_all_arcs().
        """
        return [ (i, var) for i in self.constraints[var] ]

    def add_constraint_one_way(self, i, j, filter_function):
        """Add a new constraint between variables 'i' and 'j'. The legal
        values are specified by supplying a function 'filter_function',
        that returns True for legal value pairs and False for illegal
        value pairs. This function only adds the constraint one way,
        from i -> j. You must ensure that the function also gets called
        to add the constraint the other way, j -> i, as all constraints
        are supposed to be two-way connections!
        """
        if not j in self.constraints[i]:
            # First, get a list of all possible pairs of values between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(self.domains[i], self.domains[j])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.constraints[i][j] = filter(lambda value_pair: filter_function(*value_pair), self.constraints[i][j])

    def add_all_different_constraint(self, variables):
        """Add an Alldiff constraint between all of the variables in the
        list 'variables'.
        """
        for (i, j) in self.get_all_possible_pairs(variables, variables):
            if i != j:
                self.add_constraint_one_way(i, j, lambda x, y: x != y)

    def backtracking_search(self):
        """This functions starts the CSP solver and returns the found
        solution.
        """
        # Make a so-called "deep copy" of the dictionary containing the
        # domains of the CSP variables. The deep copy is required to
        # ensure that any changes made to 'assignment' does not have any
        # side effects elsewhere.
        assignment = copy.deepcopy(self.domains)

        # Run AC-3 on all constraints in the CSP, to weed out all of the
        # values that are not arc-consistent to begin with
        self.inference(assignment, self.get_all_arcs())

        # Call backtrack with the partial assignment 'assignment'
        return self.backtrack(assignment)

    def backtrack(self, assignment):
        """The function 'Backtrack' from the pseudocode in the
        textbook.
        The function is called recursively, with a partial assignment of
        values 'assignment'. 'assignment' is a dictionary that contains
        a list of all legal values for the variables that have *not* yet
        been decided, and a list of only a single value for the
        variables that *have* been decided.
        When all of the variables in 'assignment' have lists of length
        one, i.e. when all variables have been assigned a value, the
        function should return 'assignment'. Otherwise, the search
        should continue. When the function 'inference' is called to run
        the AC-3 algorithm, the lists of legal values in 'assignment'
        should get reduced as AC-3 discovers illegal values.
        IMPORTANT: For every iteration of the for-loop in the
        pseudocode, you need to make a deep copy of 'assignment' into a
        new variable before changing it. Every iteration of the for-loop
        should have a clean slate and not see any traces of the old
        assignments and inferences that took place in previous
        iterations of the loop.
        """

        self.backtracking_call_counter += 1

        # check if assignment is done
        if self.assignment_done(assignment):
            return assignment

        # else continue with selecting an unassigned variable
        variable = self.select_unassigned_variable(assignment)

        for domain in assignment[variable]:
            # making a deep copy of 'assignment' before changing it
            new_assignment = copy.deepcopy(assignment)
            new_assignment[variable] = [domain]

            if self.inference(new_assignment, self.get_all_neighboring_arcs(variable)):
                # continue the search if there is no constraints
                result = self.backtrack(new_assignment)
                if result:
                    return result

        self.backtracking_fail_counter += 1

        return False

    def select_unassigned_variable(self, assignment):
        """The function 'Select-Unassigned-Variable' from the pseudocode
        in the textbook. Should return the name of one of the variables
        in 'assignment' that have not yet been decided, i.e. whose list
        of legal values has a length greater than one.
        """
        # returning first unassigned variable found (variable consisting of more than one value)
        for domain in assignment:
            if len(assignment[domain]) > 1:
                return domain

    def inference(self, assignment, queue):
        """The function 'AC-3' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'queue'
        is the initial queue of arcs that should be visited.
        """
        while queue:
            (xi, xj) = queue.pop()
            if self.revise(assignment, xi, xj):
                if len(assignment[xi]) is 0:
                    return False
                # adding all neighboring arcs of xi that are not in xj to the queue
                for (xk, y) in self.get_all_neighboring_arcs(xi):
                    if xk is not xj:
                        queue.append((xk, xi))
        return True

    def revise(self, assignment, i, j):
        """The function 'Revise' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'i' and
        'j' specifies the arc that should be visited. If a value is
        found in variable i's domain that doesn't satisfy the constraint
        between i and j, the value should be deleted from i's list of
        legal values in 'assignment'.
        """
        # list of inconsistencies found
        inconsistencies = []

        for iValue in assignment[i]:
            possibleValue = False
            for jValue in assignment[j]:
                # is possible value
                if (iValue, jValue) in self.constraints[i][j]:
                    possibleValue = True
                    break
            # value found that doesnt satisfy the constraint between i and j
            if not possibleValue:
                inconsistencies.append(iValue)

        # deleting values that doesnt satisfy the constraint
        for value in inconsistencies:
            assignment[i].remove(value)

        if len(inconsistencies) > 0:
            return True
        else:
            return False

    def assignment_done(self, assignment):
        """
        Checking if ALL values have been assigned a single-value.
        If so: the assignment of the variables are done.
        If not: the assignment should continue.
        """
        for key in assignment:
            if len(assignment[key]) > 1:
                return False
        return True


def create_sudoku_csp(filename):
    """Instantiate a CSP representing the Sudoku board found in the text
    file named 'filename' in the current directory.
    """
    csp = CSP()
    board = map(lambda x: x.strip(), open(filename, 'r'))

    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                csp.add_variable('%d-%d' % (row, col), map(str, range(1, 10)))
            else:
                csp.add_variable('%d-%d' % (row, col), [ board[row][col] ])

    for row in range(9):
        csp.add_all_different_constraint([ '%d-%d' % (row, col) for col in range(9) ])
    for col in range(9):
        csp.add_all_different_constraint([ '%d-%d' % (row, col) for row in range(9) ])
    for box_row in range(3):
        for box_col in range(3):
            cells = []
            for row in range(box_row * 3, (box_row + 1) * 3):
                for col in range(box_col * 3, (box_col + 1) * 3):
                    cells.append('%d-%d' % (row, col))
            csp.add_all_different_constraint(cells)

    return csp


def print_sudoku_solution(solution):
    """Convert the representation of a Sudoku solution as returned from
    the method CSP.backtracking_search(), into a human readable
    representation.
    """
    for row in range(9):
        for col in range(9):
            print solution['%d-%d' % (row, col)][0],
            if col == 2 or col == 5:
                print '|',
        print
        if row == 2 or row == 5:
            print '------+-------+------'


# Deliverable 2. & 3.
if __name__ == '__main__':
    sudoku_csp_easy = create_sudoku_csp('./sudokus/easy.txt')
    sudoku_csp_medium = create_sudoku_csp('./sudokus/medium.txt')
    sudoku_csp_hard = create_sudoku_csp('./sudokus/hard.txt')
    sudoku_csp_veryhard = create_sudoku_csp('./sudokus/veryhard.txt')

    sudoku_boards = [sudoku_csp_easy, sudoku_csp_medium, sudoku_csp_hard, sudoku_csp_veryhard]

    for idx, board in enumerate(sudoku_boards):
        if idx > 0:
            print '-'*40 + '\n'
        print 'board: #' + str(idx + 1)
        solution = board.backtracking_search()
        print_sudoku_solution(solution)
        print 'Number of backtracking calls: ' + str(board.backtracking_call_counter)
        print 'Number of backtracking failures: ' + str(board.backtracking_fail_counter) + '\n'
