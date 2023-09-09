from .prep_two_qubit import prep_two_qubit
from math import sqrt
from pytest import approx
from qiskit_aer import Aer

simulator = Aer.get_backend('aer_simulator')

def run_test_prep_two_qubit(a):
  circuit = prep_two_qubit(a).decompose(reps=2)
  circuit.save_statevector()

  res = simulator.run(circuit).result()
  state_vector = res.get_statevector().data

  for actual, expected in zip(state_vector, a):
    assert actual == approx(expected)

def test_basis_states():
  run_test_prep_two_qubit([1., 0., 0., 0.])
  run_test_prep_two_qubit([0., 1., 0., 0.])
  run_test_prep_two_qubit([0., 0., 1., 0.])
  run_test_prep_two_qubit([0., 0., 0., 1.])

def test_equal_superpositions():
  run_test_prep_two_qubit([0.5, 0.5, 0.5, 0.5])
  run_test_prep_two_qubit([-0.5, 0.5, 0.5, -0.5])
  run_test_prep_two_qubit([0.5, -0.5, 0.5, 0.5])
  run_test_prep_two_qubit([0.5, 0.5, -0.5, 0.5])
  run_test_prep_two_qubit([0.5, 0.5, 0.5, -0.5])

def test_bell_states():
  run_test_prep_two_qubit([1. / sqrt(2.), 0., 0., 1. / sqrt(2.)])
  run_test_prep_two_qubit([1. / sqrt(2.), 0., 0., -1. / sqrt(2.)])
  run_test_prep_two_qubit([0., 1. / sqrt(2.), 1. / sqrt(2.), 0.])
  run_test_prep_two_qubit([0., 1. / sqrt(2.), -1. / sqrt(2.), 0.])

def test_unequal_superpositions():
  run_test_prep_two_qubit([0.36, 0.48, 0.64, -0.48])
  run_test_prep_two_qubit([1. / sqrt(3.), -1. / sqrt(3.), 1. / sqrt(3.), 0.])
