from .two_qubit_cs_matrix import apply_two_qubit_cs_matrix
from math import pi, cos, sin
from pytest import approx
from random import random, randint
from qiskit import QuantumCircuit
from qiskit_aer import Aer

def run_test_apply_two_qubit_cs_matrix(c0, s0, c1, s1):
  circ = QuantumCircuit(2)
  circ.append(apply_two_qubit_cs_matrix(c0, s0, c1, s1), [0, 1])
  circ = circ.decompose(reps=3)

  simulator = Aer.get_backend('unitary_simulator')
  res = simulator.run(circ).result()
  matrix = res.get_unitary().data

  complete_coef = [
      [c0, 0., -s0, 0.],
      [0., c1, 0., -s1],
      [s0, 0., c0, 0.],
      [0., s1, 0., c1]]

  for actual, expected in zip(complete_coef, matrix):
    assert actual == approx(expected)

def random_one_qubit_unitary():
  theta = random() * 2 * pi
  sign = +1 if randint(0, 1) == 1 else -1
  return [[cos(theta), sign * sin(theta)], 
         [-sin(theta), sign * cos(theta)]]

def test_two_qubit_cs_matrix():
  for _ in range(1, 20):
    m0 = random_one_qubit_unitary()
    m1 = random_one_qubit_unitary()
    run_test_apply_two_qubit_cs_matrix(m0[0][0], m0[1][0], m1[0][0], m1[1][0])
