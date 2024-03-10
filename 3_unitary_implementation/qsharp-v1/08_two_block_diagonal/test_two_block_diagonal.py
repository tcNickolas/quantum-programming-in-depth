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

def run_test_apply_two_block_diagonal(n, a, b):
  # For this version of the project, only test with 2 and 3 qubits.
  if n < 2 or n > 3:
    raise NotImplementedError("This test should run on 2- or 3-qubit unitaries")

  qsharp.init(project_root='.')
  matrix = qsharp.utils.dump_operation(f"UnitaryImplementation.ApplyTwoBlockDiagonal(_, {a}, {b})", n)

  zeros = [0] * 2 ** (n - 1)
  complete_coef = [a_row + zeros for a_row in a] + \
                  [zeros + b_row for b_row in b]

  assert_matrices_equal(complete_coef, matrix)


def random_one_qubit_unitary():
  theta = random() * 2 * pi
  sign = +1 if randint(0, 1) == 1 else -1
  return [[cos(theta), sign * sin(theta)], 
         [-sin(theta), sign * cos(theta)]]

def test_two_qubit_two_block_diagonal():
  # Test on 2-qubit matrices (with 2x2 a and b).
  for j in range(1, 20):
    a = random_one_qubit_unitary()
    b = random_one_qubit_unitary()
    run_test_apply_two_block_diagonal(2, a, b)

def random_two_qubit_block_unitary():
  a = random_one_qubit_unitary()
  b = random_one_qubit_unitary()
  zeros = [0.0, 0.0]
  if randint(0, 1) == 1:
    return [a[0] + zeros, a[1] + zeros, zeros + b[0], zeros + b[1]]
  return [zeros + a[0], zeros + a[1], b[0] + zeros, b[1] + zeros]

def test_three_qubit_two_block_diagonal():
  # Test on 3-qubit matrices (with 4x4 a and b
  # of block-diagonal or anti-block-diagonal shape).
  for _ in range(1, 20):
    a = random_two_qubit_block_unitary()
    b = random_two_qubit_block_unitary()
    run_test_apply_two_block_diagonal(3, a, b)
