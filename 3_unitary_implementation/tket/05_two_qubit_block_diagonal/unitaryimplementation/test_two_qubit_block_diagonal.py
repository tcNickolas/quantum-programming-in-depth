from two_qubit_block_diagonal import apply_two_qubit_block_diagonal
from math import pi, cos, sin
from pytest import approx
from random import random, randint

def run_test_apply_two_qubit_block_diagonal(a, b):
  matrix = apply_two_qubit_block_diagonal(a, b).get_unitary()

  complete_coef = [
      a[0] + [0., 0.],
      a[1] + [0., 0.],
      [0., 0.] + b[0],
      [0., 0.] + b[1]]

  for actual, expected in zip(matrix, complete_coef):
    assert actual == approx(expected)

def random_one_qubit_unitary():
  theta = random() * 2 * pi
  sign = +1 if randint(0, 1) == 1 else -1
  return [[cos(theta), sign * sin(theta)],
         [-sin(theta), sign * cos(theta)]]

def test_two_qubit_block_diagonal():
  for _ in range(1, 20):
    a = random_one_qubit_unitary()
    b = random_one_qubit_unitary()
    run_test_apply_two_qubit_block_diagonal(a, b)
