from math import sqrt
from psiqworkbench import QPU, Qubits, Qubrick
from workbench_algorithms import ArbitraryStatePrep

# Mean state preparation routines
def get_wstate_amps(n_rows):
    'Get the array of amplitudes of the W state on n qubits.'
    wstate_amps = [0] * (2 ** n_rows)
    for i in range(n_rows):
        wstate_amps[1 << i] = 1 / sqrt(n_rows)
    return wstate_amps


class WStatePrep(ArbitraryStatePrep):
    'Qubrick to prepare a W-state'
    def __init__(self, n_rows, **kwargs):
        super().__init__(get_wstate_amps(n_rows), **kwargs)


class NQueensMeanStatePrep(Qubrick):
    'Qubrick to prepare the mean state for bit encoding of the N queens puzzle'
    def __init__(self, n_rows, **kwargs):
        super().__init__(**kwargs)
        self.n_rows = n_rows
        self.wstate_prep = WStatePrep(n_rows)
    def _compute(self, board):
        for row in range(self.n_rows):
            self.wstate_prep.compute(board[row])


# Quantum oracle implementation of classical constraints on queens placing

class OneQueenPerColumnConstraints(Qubrick):
    '''Qubrick to estimate the constraint "exactly one queen placed in each column".
    Flips the state of the target qubit if the constraint is satisfied.
    Doesn't check the last column.
    '''
    def __init__(self, n_rows, **kwargs):
        super().__init__(**kwargs)
        self.n_rows = n_rows
    def _compute(self, board, valid_column):
        # Use one fewer output qubits than columns (if all valid, last column valid automatically)
        assert valid_column.num_qubits == self.n_rows - 1
        for col in range(self.n_rows - 1):
            for row in range(self.n_rows):
                valid_column[col].x(board[row][col])


class OneQueenPerDiagonalConstraints(Qubrick):
    '''Qubrick to estimate the constraint "at most one queen placed in each diagonal".
    Flips the state of the target qubit if the constraint is satisfied.
    '''
    def __init__(self, n_rows, **kwargs):
        super().__init__(**kwargs)
        self.n_rows = n_rows
    def _compute(self, board, valid_rowpair):
        assert valid_rowpair.num_qubits == self.n_rows * (self.n_rows - 1) // 2
        ind = 0
        for row1 in range(self.n_rows):
            for row2 in range(row1 + 1, self.n_rows):
                # Flip the state of the valid_rowpair qubit if
                # the queens in these rows are on the same diagonal
                for col1 in range(self.n_rows):
                    # Check the two cells in row2 that can be on the same diagonal with (row1, col1)
                    for col2 in [col1 + (row2 - row1), col1 - (row2 - row1)]:
                        if col2 >= 0 and col2 < self.n_rows:
                            valid_rowpair[ind].x(board[row1][col1] | board[row2][col2])
                ind += 1
        # The loop flipped the qubit if the row pair was invalid - flip all qubits to make it marked if valid
        valid_rowpair.x()


class NQueensConstraints(Qubrick):
    '''Qubrick to check whether all constraints of the N queens puzzle are satisfied.
    '''
    def __init__(self, n_rows, **kwargs):
        super().__init__(**kwargs)
        self.n_rows = n_rows
        self.columns_constr = OneQueenPerColumnConstraints(n_rows)
        self.diags_constr = OneQueenPerDiagonalConstraints(n_rows)
    def _compute(self, board, valid):
        valid_column = self.alloc_temp_qreg(self.n_rows - 1, "valid_column", release_after_compute=True)
        valid_rowpair = self.alloc_temp_qreg(self.n_rows * (self.n_rows - 1) // 2, "valid_rowpair", release_after_compute=True)
        
        self.columns_constr.compute(board, valid_column)
        self.diags_constr.compute(board, valid_rowpair)

        valid.x(valid_column | valid_rowpair)

        self.diags_constr.uncompute()
        self.columns_constr.uncompute()


# Grover's search algorithm implementation

def total_bits(n_rows):
    return n_rows * n_rows + 1 + n_rows - 1 + n_rows * (n_rows - 1) // 2


def grovers_search(n_rows: int, n_iterations: int):
    qpu = QPU(num_qubits=total_bits(n_rows))

    oracle = NQueensConstraints(n_rows, never_uncompute=True)
    state_prep = NQueensMeanStatePrep(n_rows)

    board = []
    board_qubits = 0  # Same qubits, but in a single array
    for row in range(n_rows):
        board.append(Qubits(n_rows, f"board[{row}]", qpu))
        board_qubits |= board[row]
        
    minus = Qubits(1, "minus", qpu)
    minus.x()
    minus.had()

    # Prepare the mean state
    state_prep.compute(board)

    for iter in range(n_iterations):
        print(f"Iteration {iter}")

        # Apply phase oracle using phase kickback
        oracle.compute(board, minus)

        # Apply reflection about the mean
        state_prep.compute(board, dagger=True)
        (~board_qubits).reflect()
        state_prep.uncompute()

    # Measure
    res = qpu.read(target_mask=board_qubits, as_index_list=True)
    return res



def check_placement_bits(n_rows, board):
    # Results are an array of indices where queens are placed, without rows breakdown
    print(board)
    # 1. Check that there are exactly n queens
    if len(board) != n_rows:
        print(f"Incorrect queens number: expected {n_rows}, got {len(board)}")
        return False
    # 2. Check that there is one queen per row
    rows = [ind // n_rows for ind in board]
    if len(set(rows)) < n_rows:
        print(f"Two queens in a row")
        return False
    # 3. Check that there is one queen per column
    cols = [ind % n_rows for ind in board]
    if len(set(rows)) < n_rows:
        print(f"Two queens in a column")
        return False
    # 4. Check that there is at most one queen per column
    for r1 in range(n_rows):
        for r2 in range(r1 + 1, n_rows):
            diff = cols[r1] - cols[r2]
            if diff == 0 or abs(diff) == r2 - r1:
                print(f"Two queens on a diagonal: {r1},{cols[r1]} - {r2},{cols[r2]}")
                return False
    return True
