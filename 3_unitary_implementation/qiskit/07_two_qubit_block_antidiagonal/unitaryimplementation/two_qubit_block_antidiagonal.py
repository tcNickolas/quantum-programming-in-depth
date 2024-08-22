from math import atan2, isclose
from qiskit import QuantumCircuit

def apply_one_qubit(u):
  circ = QuantumCircuit(1)
  if isclose(u[0][0], -u[1][1]) and isclose(u[1][0], u[0][1]):
    circ.z(0)
  theta = atan2(u[1][0], u[0][0])
  circ.ry(2 * theta, 0)
  return circ.to_gate()

def apply_two_qubit_block_diagonal(a, b):
  circ = QuantumCircuit(2)
  circ.append(apply_one_qubit(b).control(1), [1, 0])
  circ.append(apply_one_qubit(a).control(1, ctrl_state=0), [1, 0])  
  return circ

def apply_two_qubit_cs_matrix(c0, s0, c1, s1):
  circ = QuantumCircuit(2)
  m0 = [[c0, -s0], [s0, c0]]
  m1 = [[c1, -s1], [s1, c1]]
  circ.append(apply_one_qubit(m1).control(1), [0, 1])
  circ.append(apply_one_qubit(m0).control(1, ctrl_state=0), [0, 1])  
  return circ

def apply_two_qubit_block_antidiagonal(a, b):
  circ = QuantumCircuit(2)
  id = [[1., 0.], [0., 1.]]
  minus_a = [[-a[0][0], -a[0][1]], [-a[1][0], -a[1][1]]]
  circ.append(apply_two_qubit_block_diagonal(id, minus_a), [0, 1])
  circ.append(apply_two_qubit_cs_matrix(*(0., 1.), *(0., 1.)), [0, 1])
  circ.append(apply_two_qubit_block_diagonal(id, b), [0, 1])
  return circ
