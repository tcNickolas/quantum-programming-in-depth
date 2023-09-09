from .prep_multi_qubit import prep_multi_qubit
from math import sqrt
from pytest import approx
from qiskit_aer import Aer
from random import randint, uniform

simulator = Aer.get_backend('aer_simulator')

def run_test_prep_multi_qubit(n, a):
  assert len(a) == 2 ** n

  circ = prep_multi_qubit(n, a).decompose(reps=2)
  circ.save_statevector()

  res = simulator.run(circ).result()
  state_vector = res.get_statevector().data

  for actual, expected in zip(state_vector, a):
    assert actual == approx(expected)

def test_basis_states():
  for n in range(1, 4):
    for basis in range(2 ** n):
      a = [0.] * 2 ** n
      a[basis] = 1.
      run_test_prep_multi_qubit(n, a)

def test_equal_superpositions():
  run_test_prep_multi_qubit(2, [0.5, 0.5, 0.5, 0.5])
  run_test_prep_multi_qubit(2, [0.5, -0.5, 0.5, 0.5])
  run_test_prep_multi_qubit(2, [0.5, 0.5, -0.5, 0.5])
  run_test_prep_multi_qubit(2, [0.5, 0.5, 0.5, -0.5])

def test_bell_states():
  run_test_prep_multi_qubit(2, [1. / sqrt(2.), 0., 0., 1. / sqrt(2.)])
  run_test_prep_multi_qubit(2, [1. / sqrt(2.), 0., 0., -1. / sqrt(2.)])
  run_test_prep_multi_qubit(2, [0., 1.0 / sqrt(2.), 1. / sqrt(2.), 0.])
  run_test_prep_multi_qubit(2, [0., 1.0 / sqrt(2.), -1. / sqrt(2.), 0.])

def test_unequal_superpositions():
  run_test_prep_multi_qubit(1, [0.6, 0.8])
  run_test_prep_multi_qubit(1, [0.6, -0.8])
  run_test_prep_multi_qubit(2, [0.36, 0.48, 0.64, -0.48])
  run_test_prep_multi_qubit(2, [1. / sqrt(3.), -1. / sqrt(3.), 1. / sqrt(3.), 0.])

def test_random_unequal_superpositions():
  for i in range(10):
    n = randint(2, 4)
    a = [uniform(-1.0, 1.0) for _ in range(2 ** n)]
    norm = sqrt(sum(a*a for a in a))
    a_norm = [j / norm for j in a]
    run_test_prep_multi_qubit(n, a_norm)
