from qiskit import transpile
from qiskit_aer import Aer
import pytest
from .grovers_search import *

def all_basis_states(n):
  circ = QuantumCircuit(n)
  circ.h(range(n))
  return circ.to_gate()

simulator = Aer.get_backend('aer_simulator')

test_cases = [
      (2, [0]),
      (2, [1]),
      (3, [0, 3]),
      (3, [1, 4]),
      (3, [2, 7])
    ]

@pytest.mark.parametrize("n, marked_states", test_cases)
def test_grovers_search(n, marked_states):
  marking_oracle = mark_states(n, marked_states)
  prepare_mean = all_basis_states(n)
  circ = grovers_search(n, marking_oracle, prepare_mean, 1)
  circ = transpile(circ, backend=simulator)
  res_map = simulator.run(circ, shots=100).result().get_counts()
  # For this test, results should only be one of the marked states
  assert len(res_map) <= len(test_cases)
  # Check that it is indeed the case
  for res_bitstring in res_map.keys():
    print(res_bitstring)
    # Qiskit measurement results are in reversed order compared to qubit order
    res_int = int(res_bitstring[::-1], 2)
    assert res_int in marked_states
