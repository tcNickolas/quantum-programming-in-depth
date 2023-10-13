from .one_qubit_unitary import apply_one_qubit
from math import pi, cos, sin
from random import random, randint
from pytest import approx
from qiskit import QuantumCircuit
from qiskit_aer import Aer

def run_test_apply_one_qubit(c):
  assert len(c) == 2
  for row in c:
    assert len(row) == 2

  circ = QuantumCircuit(1)
  circ.append(apply_one_qubit(c), [0])
  circ = circ.decompose()

  simulator = Aer.get_backend('unitary_simulator')
  res = simulator.run(circ).result()
  matrix = res.get_unitary().data

  for actual, expected in zip(c, matrix):
    assert actual == approx(expected)

def test_diag_antidiag():
  run_test_apply_one_qubit([[1., 0.], [0., 1.]])
  run_test_apply_one_qubit([[1., 0.], [0., -1.]])
  run_test_apply_one_qubit([[-1., 0.], [0., 1.]])
  run_test_apply_one_qubit([[-1., 0.], [0., -1.]])
  run_test_apply_one_qubit([[0., 1.], [1., 0.]])
  run_test_apply_one_qubit([[0., 1.], [-1., 0.]])
  run_test_apply_one_qubit([[0., -1.], [1., 0.]])
  run_test_apply_one_qubit([[0., -1.], [-1., 0.]])

def random_one_qubit_unitary():
  theta = random() * 2 * pi
  sign = +1 if randint(0, 1) == 1 else -1
  return [[cos(theta), sign * sin(theta)], 
         [-sin(theta), sign * cos(theta)]]

def test_dense():
  for _ in range(1, 20):
    run_test_apply_one_qubit(random_one_qubit_unitary())
