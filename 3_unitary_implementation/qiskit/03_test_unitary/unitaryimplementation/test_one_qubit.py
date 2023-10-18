from .one_qubit_unitary import apply_one_qubit
from math import pi, cos, sin
from random import random, randint
from pytest import approx
from qiskit.quantum_info import Operator

def run_test_apply_one_qubit(u):
  assert len(u) == 2
  for row in u:
    assert len(row) == 2

  op = Operator(apply_one_qubit(u))
  matrix = op.data

  for actual, expected in zip(matrix, u):
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
