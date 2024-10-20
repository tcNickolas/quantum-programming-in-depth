from cmath import isclose
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Operator
import pytest
from .oracles import *

def f_mark_states(args, marked_states):
  # Use big endian to convert Boolean array to integer
  arg = int("".join(["1" if a else "0" for a in args]), 2)
  return arg in marked_states


simulator = Aer.get_backend('aer_simulator')

test_cases = [
      (1, []),
      (1, [1]),
      (2, [1]),
      (2, [2]),
      (2, [0, 3]),
      (3, [0, 3, 6]),
      (3, [1, 3, 5, 7])
    ]


@pytest.mark.parametrize("n, marked_states", test_cases)
def test_mark_states(n, marked_states):
  format_str = f"{{:0>{n}b}}"
  for input in range(2 ** n):
    input_str = format_str.format(input)
    input_be = [input_str[i] == '1' for i in range(n)]

    circ = QuantumCircuit(n + 1)
    for i in range(n):
      if input_be[i]:
        circ.x(i)

    circ.append(mark_states(n, marked_states), range(n + 1))

    expected = f_mark_states(input_be, marked_states)
    if expected:
      circ.x(n)

    for i in range(n):
      if input_be[i]:
        circ.x(i)

    circ = circ.decompose(reps=2)
    circ.save_statevector()

    res = simulator.run(circ).result()
    state_vector = res.get_statevector().data

    non_zeros = [not isclose(amp, 0, abs_tol=1e-9) for amp in state_vector]
    if any(non_zeros[1:]):
      # Either result is incorrect or inputs are modified.
      # Result is stored in most significant bit, input - in least significant bit
      prefix = f"Error for x={input}:"
      count = non_zeros.count(True)
      if count > 1:
        raise Exception(f"{prefix} the state should not be a superposition")

      index = non_zeros.index(True)
      if index // (2 ** (n - 1)) > 0:
        raise Exception(f"{prefix} expected {expected}, got {not expected}")
      else:
        raise Exception(f"{prefix} the state of the input qubits changed")


@pytest.mark.parametrize("n, marked_states", test_cases)
def test_phase_oracle(n, marked_states):
  marking_oracle = mark_states(n, marked_states)
  op = Operator(phase_oracle(n, marking_oracle))
  matrix = op.data

  print(matrix)

  # Identity matrix
  complete_coef = []
  for state in range(2 ** (n + 1)):
    row = [0] * 2 ** (n + 1)
    row[state] = 1
    complete_coef += [row]
  # Mark only the states where phase is flipped
  for state in marked_states:
    stateLE = int((f"{{:0>{n}b}}".format(state))[::-1], 2)
    complete_coef[stateLE][stateLE] = -1

  for actual, expected in zip(matrix, complete_coef):
    assert actual == pytest.approx(expected)
