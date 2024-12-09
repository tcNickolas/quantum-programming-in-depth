from math import atan2, cos, isclose, pi, sin
from random import randint, random
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from .reconstruct_unitary import reconstruct_unitary

def apply_one_qubit(u):
  circ = QuantumCircuit(1)
  if isclose(u[0][0], -u[1][1]) and isclose(u[1][0], u[0][1]):
    circ.z(0)
  theta = atan2(u[1][0], u[0][0])
  circ.ry(2 * theta, 0)
  return circ.to_gate()

def random_one_qubit_unitary():
  theta = random() * 2 * pi
  sign = +1 if randint(0, 1) == 1 else -1
  return [[cos(theta), sign * sin(theta)], 
         [-sin(theta), sign * cos(theta)]]


def test_reconstruct_unitary():
  for _ in range(10):
    matrix = random_one_qubit_unitary()
    unitary = apply_one_qubit(matrix)

    matrix_res = reconstruct_unitary(unitary)

    print(f"Actual matrix {matrix}, returned {matrix_res}")

  for j in range(2):
    for k in range(2):
      if abs(matrix[j][k] - matrix_res[j][k]) > 0.1:
        print(f"Incorrect coefficient at [{j}][{k}]: expected {matrix[j][k]}, got {matrix_res[j][k]}")
