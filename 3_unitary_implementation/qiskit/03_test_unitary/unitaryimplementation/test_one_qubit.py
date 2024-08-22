from math import cos, pi, sin
from random import randint, random
import pytest
from qiskit.quantum_info import Operator
from .one_qubit_unitary import apply_one_qubit

@pytest.mark.parametrize("u",
    [ [[1.0, 0.0], [0.0, 1.0]],
      [[1.0, 0.0], [0.0, -1.0]],
      [[-1.0, 0.0], [0.0, 1.0]],
      [[-1.0, 0.0], [0.0, -1.0]],
      [[0.0, 1.0], [1.0, 0.0]],
      [[0.0, 1.0], [-1.0, 0.0]],
      [[0.0, -1.0], [1.0, 0.0]],
      [[0.0, -1.0], [-1.0, 0.0]] ])
def test_apply_one_qubit(u):
  assert len(u) == 2
  for row in u:
    assert len(row) == 2

  op = Operator(apply_one_qubit(u))
  matrix = op.data

  for actual, expected in zip(matrix, u):
    assert actual == pytest.approx(expected)

def random_one_qubit_unitary():
  theta = random() * 2 * pi
  sign = +1 if randint(0, 1) == 1 else -1
  return [[cos(theta), sign * sin(theta)], 
         [-sin(theta), sign * cos(theta)]]

def test_dense():
  for _ in range(1, 20):
    test_apply_one_qubit(random_one_qubit_unitary())
