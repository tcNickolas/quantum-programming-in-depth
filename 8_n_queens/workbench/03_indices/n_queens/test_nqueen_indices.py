from psiqworkbench import QPU, Qubits
from .n_queens import *
import pytest
from numpy import kron

def test_mean_prep():
    qpu = QPU()
    for n in range(2, 5):
        bitsize = bits_per_row(n)
        qpu.reset(n * bitsize)
        board = []
        for row in range(n):
            board.append(Qubits(bitsize, f"board[{row}]", qpu))
        state_prep = NQueensMeanStatePrep(n)
        state_prep.compute(board)

        state_vector = qpu.pull_state()
        mean = mean_amps(n)
        expected = mean
        for _ in range(n - 1):
            expected = kron(expected, mean)
        assert state_vector == pytest.approx(expected)


def test_nqueens_oracle():
    n_rows = 4
    bitsize = bits_per_row(n_rows)
    n_total = total_bits(n_rows)

    qpu = QPU(filters=['>>bit-qpu>>'])
    oracle = NQueensConstraints(n_rows)

    # Use the same optimization for the test as for the oracle: 
    # guarantee that each row already has at most one queen
    n_tests = n_rows ** n_rows
    for input_index in range(n_tests):
        qpu.reset(n_total)
        board = []
        board_qubits = 0  # Same qubits, but in a single array
        for row in range(n_rows):
            board.append(Qubits(bitsize, f"board[{row}]", qpu))
            board_qubits |= board[row]
        y = Qubits(1, "y", qpu)

        # Convert input_index into a LE integer encoding
        input_int = 0
        cols = []        
        ind = input_index
        for row in range(n_rows):
            col = ind % n_rows
            cols.append(col)
            ind //= n_rows
            input_int |= (1 << (row * bitsize)) * col

        # Initialize the input with a basis state (LE)
        board_qubits.x(input_int)
        oracle.compute(board, y)

        # Measure (the code uses no gates to introduce superposition)
        res_int = board_qubits.read()

        if res_int != input_int:
            raise Exception(f"Error for x={input_int}: the state of the input qubits changed")

        # Same measurement in a different format to match the way the check is written
        expected = check_placement_indices(n_rows, cols)
        actual = y.read() > 0
        if expected != actual:
            raise Exception(f"Error for evaluating x={input_int}: expected {expected}, got {actual}")
