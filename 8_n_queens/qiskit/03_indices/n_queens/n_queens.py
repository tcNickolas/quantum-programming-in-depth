from math import sqrt
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import CDKMRippleCarryAdder, StatePreparation
from qiskit.circuit.library.standard_gates import XGate, ZGate

def bits_per_row(n):
  return (n - 1).bit_length()


def total_indices(n):
  return n * bits_per_row(n) + n * (n - 1) // 2 + 3


def prep_mean_indices(n):
  """Prepare the mean state for the indices encoding"""
  # Prepare equal superposition of the first n basis states on each row of n qubits
  bitsize = bits_per_row(n)
  mean_amps = [1 / sqrt(n)] * n + [0] * (2 ** bitsize - n)
  meanstateprep = StatePreparation(mean_amps)
  circ = QuantumCircuit(n * bitsize)
  for r in range(n):
    circ.append(meanstateprep, range(r * bitsize, (r + 1) * bitsize))
  return circ.to_gate()


def oracle_indices(n):
  """The oracle for the N queens problem."""
  # The presence of a queen in row r and column c is described 
  # with indices[r] - bitSize bits starting with x[bitSize * r] that encode the integer c in big endian.
  bitsize = bits_per_row(n)

  adder = CDKMRippleCarryAdder(bitsize).to_gate()

  x = QuantumRegister(n * bitsize)
  y = QuantumRegister(1)
  invalid_rowpair = QuantumRegister(n * (n - 1) // 2)
  carryin = QuantumRegister(1)
  carryout = QuantumRegister(1)

  circ = QuantumCircuit(x, invalid_rowpair, carryin, carryout, y)
  circ.x(carryout)

  def one_queen_per_column_diagonal():
    """Evaluate the constraint of one queen per column/diagonal."""
    ind = 0
    for r1 in range(n):
      for r2 in range(r1 + 1, n):
        # Compute the difference between indices[r1] and indices[r2]
        diff_inds = carryin[:] + x[bitsize * r2:bitsize * (r2+1)] + x[bitsize * r1:bitsize * (r1+1)] + carryout[:]
        circ.append(adder.inverse(), diff_inds)
        for diff in [0, r1 - r2, r2 - r1]:
          circ.append(XGate().control(bitsize + 1, ctrl_state=diff + (2 ** bitsize)), 
                      x[bitsize * r1:bitsize * (r1+1)] + carryout[:] + [invalid_rowpair[ind]])
        circ.append(adder, diff_inds)

        ind += 1

  one_queen_per_column_diagonal()
  circ.append(XGate().control(len(invalid_rowpair), ctrl_state=0),
              invalid_rowpair[:] + y[:])
  one_queen_per_column_diagonal()

  circ.x(carryout)

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
  n_bits = total_indices(n_rows)
  n_x = n_rows * bits_per_row(n_rows)

  circ = QuantumCircuit(n_bits, n_x)
  circ.append(prep_mean_indices(n_rows), range(n_x))

  for _ in range(n_iterations):
    # Apply phase oracle
    circ.append(phase_oracle(n_bits, oracle_indices(n_rows)), range(n_bits))
    # Apply reflection about the mean
    circ.append(prep_mean_indices(n_rows).inverse(), range(n_x))
    circ.x(range(n_x))
    circ.append(ZGate().control(n_x - 1), range(n_x))
    circ.x(range(n_x))
    circ.append(prep_mean_indices(n_rows), range(n_x))

  circ.measure(range(n_x), range(n_x))

  return circ


def check_placement_indices(n, bits):
  bitsize = bits_per_row(n)
  indices = [int(bits[bitsize * row:bitsize * (row + 1)], 2) for row in range(n)]
  for index in indices:
    if index < 0 or index >= n:
      return False
  return check_one_queen_per_column_diagonal(n, indices)


def check_one_queen_per_column_diagonal(n, indices):
  for r1 in range(n):
    for r2 in range(r1 + 1, n):
      diff = indices[r1] - indices[r2]
      if diff == 0 or abs(diff) == r2 - r1:
        # print(f"Queens ({r1}, {indices[r1]}) and ({r2}, {indices[r2]}) on column or diagonal")
        return False
  return True
