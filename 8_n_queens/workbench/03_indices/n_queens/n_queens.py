from math import sqrt
from psiqworkbench import QPU, Qubits, Qubrick, QUInt
from workbench_algorithms import ArbitraryStatePrep

# Mean state preparation routines
def bits_per_row(n_rows):
    return (n_rows - 1).bit_length()

def mean_amps(n_rows):
    bitsize = bits_per_row(n_rows)
    return [1 / sqrt(n_rows)] * n_rows + [0] * (2 ** bitsize - n_rows)


class NQueensMeanStatePrep(Qubrick):
    'Qubrick to prepare the mean state for indices encoding of the N queens puzzle'
    def __init__(self, n_rows, **kwargs):
        super().__init__(**kwargs)
        self.n_rows = n_rows
        self.state_prep = ArbitraryStatePrep(mean_amps(n_rows))
    def _compute(self, board):
        for row in range(self.n_rows):
            self.state_prep.compute(board[row])


# Quantum oracle implementation of classical constraints on queens placing
class OneQueenPerColumnDiagonalConstraints(Qubrick):
    '''Qubrick to estimate the constraint "at most one queen placed in each diagonal and each column".
    Flips the state of the target qubit if the constraint is satisfied.
    '''
    def __init__(self, n_rows, **kwargs):
        super().__init__(**kwargs)
        self.n_rows = n_rows
    def _compute(self, board, valid_rowpair):
        # board[row] is bitsize bits encoding a little-endian integer - the column index of the queen in this row
        bitsize = bits_per_row(self.n_rows)
        assert valid_rowpair.num_qubits == self.n_rows * (self.n_rows - 1) // 2

        aux = self.alloc_temp_qreg(1, "aux", release_after_compute=True)  # The |1> bit used as MSB to keep subtraction from overflowing
        aux.x()

        ind = 0
        for row1 in range(self.n_rows):
            for row2 in range(row1 + 1, self.n_rows):
                # Compute the difference between indices[r1] and indices[r2]
                # Flip the state of the valid_rowpair qubit if
                # the queens in these rows are on the same diagonal or column
                reg1 = QUInt(board[row1] | aux)
                reg2 = QUInt(board[row2])
                reg1 -= reg2  # Now reg1 is the difference between two indices

                for diff in [0, row1 - row2, row2 - row1]:
                    with reg1 == diff + (1 << bitsize) as cond:
                        valid_rowpair[ind].x(cond)

                reg1 += reg2  # Uncompute subtraction

                ind += 1

        # The loop flipped the qubit if the row pair was invalid - flip all qubits to make it marked if valid
        valid_rowpair.x()

        aux.x()


class NQueensConstraints(Qubrick):
    '''Qubrick to check whether all constraints of the N queens puzzle are satisfied.
    '''
    def __init__(self, n_rows, **kwargs):
        super().__init__(**kwargs)
        self.n_rows = n_rows
        self.constr = OneQueenPerColumnDiagonalConstraints(n_rows)
    def _compute(self, board, valid):
        valid_rowpair = self.alloc_temp_qreg(self.n_rows * (self.n_rows - 1) // 2, "valid_rowpair", release_after_compute=True)
        
        with self.constr.computed(board, valid_rowpair):
            valid.x(valid_rowpair)
        

# Grover's search algorithm implementation

def total_bits(n_rows):
    return n_rows * bits_per_row(n_rows) + n_rows * (n_rows - 1) // 2 + 2
    


def grovers_search(n_rows: int, n_iterations: int):
    qpu = QPU(num_qubits=total_bits(n_rows))
    bitsize = bits_per_row(n_rows)

    oracle = NQueensConstraints(n_rows)
    state_prep = NQueensMeanStatePrep(n_rows)

    board = []
    board_qubits = 0  # Same qubits, but in a single array
    for row in range(n_rows):
        board.append(Qubits(bitsize, f"board[{row}]", qpu))
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
    res = [board[row].read() for row in range(n_rows)]
    return res



def check_placement_indices(n_rows, board):
    # Results are an array of indices where queens are placed with rows breakdown
    print(board)
    # 1. Check that there are exactly n queens - don't need, each board[row] is one queen
    # 2. Check that there is one queen per row - don't need
    # 3. Check that there is one queen per column
    # 4. Check that there is at most one queen per column
    for r1 in range(n_rows):
        for r2 in range(r1 + 1, n_rows):
            diff = board[r1] - board[r2]
            if diff == 0:
                # print(f"Two queens in the same column: {r1},{board[r1]} - {r2},{board[r2]}")
                return False
            if abs(diff) == r2 - r1:
                # print(f"Two queens on a diagonal: {r1},{board[r1]} - {r2},{board[r2]}")
                return False
    return True