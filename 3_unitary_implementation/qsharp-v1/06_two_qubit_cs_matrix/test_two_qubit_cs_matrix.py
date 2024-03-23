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

def run_test_apply_two_qubit_cs_matrix(c0, s0, c1, s1):
  qsharp.init(project_root='.')
  matrix = dump_operation(f"UnitaryImplementation.ApplyTwoQubitCSMatrix(_, ({c0}, {s0}), ({c1}, {s1}))", 2)

  complete_coef = [
      [c0, 0., -s0, 0.],
      [0., c1, 0., -s1],
      [s0, 0., c0, 0.],
      [0., s1, 0., c1]]

  assert_matrices_equal(complete_coef, matrix)


def random_one_qubit_unitary():
  theta = random() * 2 * pi
  sign = +1 if randint(0, 1) == 1 else -1
  return [[cos(theta), sign * sin(theta)], 
         [-sin(theta), sign * cos(theta)]]

def test_dense():
  for _ in range(1, 20):
    m0 = random_one_qubit_unitary()
    m1 = random_one_qubit_unitary()
    run_test_apply_two_qubit_cs_matrix(m0[0][0], m0[1][0], m1[0][0], m1[1][0])
