from .arbitrary_cs_matrix import apply_arbitrary_cs_matrix
from math import pi, cos, sin
from pytest import approx
from random import random, randint
from qiskit import QuantumCircuit
from qiskit_aer import Aer

def run_test_apply_arbitrary_cs_matrix(n, cs):
  circ = QuantumCircuit(n)
  circ.append(apply_arbitrary_cs_matrix(n, cs), range(n))
  circ = circ.decompose(reps=3)

  simulator = Aer.get_backend('unitary_simulator')
  res = simulator.run(circ).result()
  matrix = res.get_unitary().data

  print(matrix)

  complete_coef = []
  for (i, (c, s)) in enumerate(cs):
    z_before = [0] * i
    z_after = [0] * (2 ** (n - 1) - i - 1)
    complete_coef += [z_before + [c] + z_after + z_before + [-s] + z_after]
  for (i, (c, s)) in enumerate(cs):
    z_before = [0] * i
    z_after = [0] * (2 ** (n - 1) - i - 1)
    complete_coef += [z_before + [s] + z_after + z_before + [c] + z_after]

  print(complete_coef)

  for actual, expected in zip(complete_coef, matrix):
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
