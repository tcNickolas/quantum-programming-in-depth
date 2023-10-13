from .two_qubit_block_antidiagonal import apply_two_qubit_block_antidiagonal
from math import pi, cos, sin
from pytest import approx
from random import random, randint
from qiskit import QuantumCircuit
from qiskit_aer import Aer

def run_test_apply_two_qubit_block_antidiagonal(a, b):
  circ = QuantumCircuit(2)
  circ.append(apply_two_qubit_block_antidiagonal(a, b), [0, 1])
  circ = circ.decompose(reps=4)

  simulator = Aer.get_backend('unitary_simulator')
  res = simulator.run(circ).result()
  matrix = res.get_unitary().data

  complete_coef = [
      [0., 0.] + a[0],
      [0., 0.] + a[1],
      b[0] + [0., 0.],
      b[1] + [0., 0.]]

  for actual, expected in zip(complete_coef, matrix):
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
    run_test_apply_two_qubit_block_antidiagonal(a, b)
