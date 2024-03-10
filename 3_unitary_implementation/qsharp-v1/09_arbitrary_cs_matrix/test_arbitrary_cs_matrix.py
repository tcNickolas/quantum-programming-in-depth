from math import cos, pi, sin
from random import randint, random
import pytest
import qsharp
import qsharp.utils

def assert_matrices_equal(u, v):
  # Check matrix dimensions
  n = len(u)
  assert len(u) == n
  for row in range(n):
    assert len(u[row]) == n
    assert len(v[row]) == n

  # Find first non-zero element to use for normalization
  first_row = -1
  first_col = -1
  for row in range(n):
    for col in range(n):
      if abs(u[row][col]) > 1E-9:
        first_row = row
        first_col = col
        break
    if first_row > -1:
      break

  # Compare element-wise, normalizing elements
  for row in range(len(u)):
    for col in range(len(u)):
      assert u[row][col] / u[first_row][first_col] == \
        pytest.approx(v[row][col] / v[first_row][first_col], rel=1e-4)

def run_test_apply_arbitrary_cs_matrix(n, cs):
  qsharp.init(project_root='.')
  matrix = qsharp.utils.dump_operation(f"UnitaryImplementation.ApplyArbitraryCSMatrix(_, {cs})", n)

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
