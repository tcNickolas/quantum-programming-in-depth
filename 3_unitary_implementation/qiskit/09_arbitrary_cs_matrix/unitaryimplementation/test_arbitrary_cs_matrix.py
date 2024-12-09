from math import cos, pi, sin
from random import randint, random
from qiskit.quantum_info import Operator
from pytest import approx
from .arbitrary_cs_matrix import apply_arbitrary_cs_matrix

def run_test_apply_arbitrary_cs_matrix(n, cs):
  op = Operator(apply_arbitrary_cs_matrix(n, cs))
  matrix = op.data

  complete_coef = []
  for (i, (c, s)) in enumerate(cs):
    z_before = [0] * i
    z_after = [0] * (2 ** (n - 1) - i - 1)
    complete_coef += [z_before + [c] + z_after + z_before + [-s] + z_after]
  for (i, (c, s)) in enumerate(cs):
    z_before = [0] * i
    z_after = [0] * (2 ** (n - 1) - i - 1)
    complete_coef += [z_before + [s] + z_after + z_before + [c] + z_after]

  for actual, expected in zip(matrix, complete_coef):
    assert actual == approx(expected)

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
