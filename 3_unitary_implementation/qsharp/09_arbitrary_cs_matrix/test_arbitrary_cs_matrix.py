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

def run_test_apply_arbitrary_cs_matrix(n, cs):
  qsharp.init(project_root='.')
  matrix = dump_operation(f"UnitaryImplementation.ApplyArbitraryCSMatrix(_, {cs})", n)

  complete_coef = []
  for (i, (c, s)) in enumerate(cs):
    z_before = [0] * i
    z_after = [0] * (2 ** (n - 1) - i - 1)
    complete_coef += [z_before + [c] + z_after + z_before + [-s] + z_after]
  for (i, (c, s)) in enumerate(cs):
    z_before = [0] * i
    z_after = [0] * (2 ** (n - 1) - i - 1)
    complete_coef += [z_before + [s] + z_after + z_before + [c] + z_after]

  assert_matrices_equal(complete_coef, matrix)


def random_one_qubit_unitary():
  theta = random() * 2 * pi
  sign = +1 if randint(0, 1) == 1 else -1
  return [[cos(theta), sign * sin(theta)], 
         [-sin(theta), sign * cos(theta)]]

def test_arbitrary_cs_matrix():
  for _ in range(1, 20):
    n = randint(2, 5)
    cs = []
    for _ in range(2 ** (n - 1)):
      mi = random_one_qubit_unitary()
      cs += [(mi[0][0], mi[1][0])]
    run_test_apply_arbitrary_cs_matrix(n, cs)
