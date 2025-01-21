from cmath import isclose
from time import time
from qiskit import transpile
from qiskit_aer import AerSimulator
import pytest
from .n_queens import *

simulator = AerSimulator(method='statevector')

testcases = []
for start in range(16):
  testcases.append(range(start * 16, (start + 1) * 16))

@pytest.mark.parametrize("rng", testcases)
def test_nqueens(rng):
  n_rows = 4
  n_inputs = n_rows * bits_per_row(n_rows)
  n_total = total_indices(n_rows)

  for input_int in rng:
    start_time = time()
    input_str = "{:0>16b}".format(input_int)

    circ = QuantumCircuit(n_total)
    # Initialize only the input register
    for i in range(n_inputs):
      if input_str[i] == '1':
        circ.x(i)

    circ.append(oracle_indices(n_rows).to_gate(), range(n_total))

    expected = check_placement_indices(n_rows, input_str)
    if expected:
      circ.x(n_total - 1)

    for i in range(n_inputs):
      if input_str[i] == '1':
        circ.x(i)

    circ = transpile(circ, backend=simulator)
    circ.save_statevector()

    res = simulator.run(circ).result()
    state_vector = res.get_statevector().data    

    non_zeros = [not isclose(amp, 0, abs_tol=1e-9) for amp in state_vector]
    if any(non_zeros[1:]):
      # Either result is incorrect or inputs are modified.
      # Result is stored in most significant bit, input - in the least significant bits
      prefix = f"Error for x={input_str}:"
      count = non_zeros.count(True)
      if count > 1:
        raise Exception(f"{prefix} the state should not be a superposition")

      index = non_zeros.index(True)
      if index // (2 ** (n_total - 1)) > 0:
        raise Exception(f"{prefix} expected {expected}, got {not expected}")
      else:
        raise Exception(f"{prefix} the state of the input qubits was modified")

    end_time = time()
    print(f"{input_str} ok ({round(end_time - start_time)} sec)", flush=True)
