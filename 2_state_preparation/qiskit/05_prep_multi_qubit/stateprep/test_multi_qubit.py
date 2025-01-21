from math import sqrt
from random import randint, uniform
from qiskit import transpile
from qiskit_aer import AerSimulator
import pytest
from .prep_multi_qubit import prep_multi_qubit

simulator = AerSimulator(method='statevector')

def run_test_prep_multi_qubit(n, a):
  assert len(a) == 2 ** n

  circ = prep_multi_qubit(n, a)
  circ.save_statevector()

  circ = transpile(circ, backend=simulator)
  res = simulator.run(circ).result()
  state_vector = res.get_statevector().data

  assert state_vector == pytest.approx(a)

def test_basis_states():
  for n in range(1, 4):
    for basis in range(2 ** n):
      a = [0.] * 2 ** n
      a[basis] = 1.
      run_test_prep_multi_qubit(n, a)

@pytest.mark.parametrize("a",
    [ [0.5, 0.5, 0.5, 0.5],
      [-0.5, 0.5, 0.5, -0.5],
      [0.5, -0.5, 0.5, 0.5],
      [0.5, 0.5, -0.5, 0.5],
      [0.5, 0.5, 0.5, -0.5],
      [1. / sqrt(2.), 0., 0., 1. / sqrt(2.)],
      [1. / sqrt(2.), 0., 0., -1. / sqrt(2.)],
      [0., 1. / sqrt(2.), 1. / sqrt(2.), 0.],
      [0., 1. / sqrt(2.), -1. / sqrt(2.), 0.],
      [0.36, 0.48, 0.64, -0.48],
      [1. / sqrt(3.), -1. / sqrt(3.), 1. / sqrt(3.), 0.]
    ])
def test_prep_two_qubits(a):
  run_test_prep_multi_qubit(2, a)

def test_random_unequal_superpositions():
  for i in range(10):
    n = randint(2, 4)
    a = [uniform(-1.0, 1.0) for _ in range(2 ** n)]
    norm = sqrt(sum(a*a for a in a))
    a_norm = [j / norm for j in a]
    run_test_prep_multi_qubit(n, a_norm)
