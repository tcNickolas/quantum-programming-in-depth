from math import cos, pi, sin
from random import randint, random
import pytest
import qsharp
from qsharp.utils import dump_operation

def assert_matrices_equal(u, v):
  # Check matrix dimensions
  n = len(u)
  assert len(v) == n
  for row in range(n):
    assert len(u[row]) == n and len(v[row]) == n

  # Find global phase difference
  global_phase = -2
  for row in range(n):
    for col in range(n):
      if abs(u[row][col]) > 1E-9:
        global_phase = v[row][col] / u[row][col]
        break
    if abs(global_phase) < 1.5:
      break

  # Compare element-wise, normalizing elements
  for row in range(len(u)):
    for col in range(len(u)):
      assert u[row][col] * global_phase == \
        pytest.approx(v[row][col], abs=1e-4)

def run_test_apply_two_qubit_block_antidiagonal(a, b):
  qsharp.init(project_root='.')
  matrix = dump_operation(f"UnitaryImplementation.ApplyTwoQubitBlockAntiDiagonal(_, {a}, {b})", 2)

  complete_coef = [
      [0., 0.] + a[0],
      [0., 0.] + a[1],
      b[0] + [0., 0.],
      b[1] + [0., 0.]]

  assert_matrices_equal(complete_coef, matrix)


def random_one_qubit_unitary():
  theta = random() * 2 * pi
  sign = +1 if randint(0, 1) == 1 else -1
  return [[cos(theta), sign * sin(theta)], 
         [-sin(theta), sign * cos(theta)]]

def test_dense():
  for _ in range(1, 20):
    a = random_one_qubit_unitary()
    b = random_one_qubit_unitary()
    run_test_apply_two_qubit_block_antidiagonal(a, b)
