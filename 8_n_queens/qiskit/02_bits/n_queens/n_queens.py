from math import sqrt
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import StatePreparation
from qiskit.circuit.library.standard_gates import XGate, ZGate


def total_bits(n):
  return n * n + 1 + n - 1 + n * (n - 1) // 2


def prep_mean_bits(n):
  """Prepare the mean state for the bits encoding"""
  # Get the array of amplitudes of the W state on n qubits.
  wstate_amps = [0] * (2 ** n)
  for i in range(n):
    wstate_amps[1 << i] = 1 / sqrt(n)

  # Prepare W state on each row of n qubits
  wstateprep = StatePreparation(wstate_amps)
  circ = QuantumCircuit(n * n)
  for r in range(n):
    circ.append(wstateprep, range(r * n, (r + 1) * n))
  return circ.to_gate()


def oracle_bits(n):
  """The oracle for the N queens problem."""
  # The presence of a queen in row r and column c is described with x[r * n + c].
  x = QuantumRegister(n * n, 'x')
  y = QuantumRegister(1, 'y')
  valid_column = QuantumRegister(n - 1, 'valid_column')
  invalid_rowpair = QuantumRegister(n * (n - 1) // 2, 'invalid_rowpair')

  circ = QuantumCircuit(x, valid_column, invalid_rowpair, y)

  def one_queen_per_column():
    """Evaluate the constraint of one queen per column."""
    for c in range(n - 1):
      for r in range(n):
        circ.cx(x[r * n + c], valid_column[c])

  def one_queen_per_diagonal():
    """Evaluate the constraint of one queen per diagonal."""
    ind = 0
    for r1 in range(n):
      for r2 in range(r1 + 1, n):
        for c1 in range(n):
          for c2 in [c1 + (r2 - r1), c1 - (r2 - r1)]:
            if c2 >= 0 and c2 < n:
              circ.ccx(x[r1 * n + c1], x[r2 * n + c2], invalid_rowpair[ind])
        ind += 1
    circ.x(invalid_rowpair)

  one_queen_per_column()
  one_queen_per_diagonal()
  circ.append(XGate().control(len(valid_column) + len(invalid_rowpair)),
              valid_column[:] + invalid_rowpair[:] + y[:])
  one_queen_per_column()
  one_queen_per_diagonal()
  
  return circ


def phase_oracle(n, marking_oracle):
  circ = QuantumCircuit(n)
  circ.h(n-1)
  circ.z(n-1)
  circ.append(marking_oracle.to_gate(), range(n))
  circ.z(n-1)
  circ.h(n-1)
  return circ.to_gate()


def grovers_search(n_rows, n_iterations):
  n_bits = total_bits(n_rows)
  n_x = n_rows * n_rows

  circ = QuantumCircuit(n_bits, n_x)
  circ.append(prep_mean_bits(n_rows), range(n_x))

  for _ in range(n_iterations):
    # Apply phase oracle
    circ.append(phase_oracle(n_bits, oracle_bits(n_rows)), range(n_bits))
    # Apply reflection about the mean
    circ.append(prep_mean_bits(n_rows).inverse(), range(n_x))
    circ.x(range(n_x))
    circ.append(ZGate().control(n_x - 1), range(n_x))
    circ.x(range(n_x))
    circ.append(prep_mean_bits(n_rows), range(n_x))

  circ.measure(range(n_x), range(n_x))

  return circ


def check_placement_bits(n, bits):
  board = [bits[n * row:n * (row + 1)] for row in range(n)]
  # One queen per row
  for r in range(n):
    n_q = 0
    for c in range(n):
      if board[r][c] == '1':
        n_q += 1
    if n_q != 1:
      return False
  indices = [row.index('1') for row in board]
  return check_one_queen_per_column_diagonal(n, indices)


def check_one_queen_per_column_diagonal(n, indices):
  for r1 in range(n):
    for r2 in range(r1 + 1, n):
      diff = indices[r1] - indices[r2]
      if diff == 0 or abs(diff) == r2 - r1:
        return False
  return True
