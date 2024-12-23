from math import cos, pi, sin
from random import randint, random
import qsharp
from qsharp.utils import dump_operation
import pytest

def run_test_apply_two_qubit_block_diagonal(a, b):
  qsharp.init(project_root='.')
  matrix = dump_operation(f"UnitaryImplementation.ApplyTwoQubitBlockDiagonal(_, {a}, {b})", 2)

  complete_coef = [
      a[0] + [0., 0.],
      a[1] + [0., 0.],
      [0., 0.] + b[0],
      [0., 0.] + b[1]]

  for actual, expected in zip(matrix, complete_coef):
    assert actual == pytest.approx(expected, abs=1e-6)


def random_one_qubit_unitary():
  theta = random() * 2 * pi
  sign = +1 if randint(0, 1) == 1 else -1
  return [[cos(theta), sign * sin(theta)], 
         [-sin(theta), sign * cos(theta)]]


def test_dense():
  for _ in range(1, 20):
    a = random_one_qubit_unitary()
    b = random_one_qubit_unitary()
    run_test_apply_two_qubit_block_diagonal(a, b)
