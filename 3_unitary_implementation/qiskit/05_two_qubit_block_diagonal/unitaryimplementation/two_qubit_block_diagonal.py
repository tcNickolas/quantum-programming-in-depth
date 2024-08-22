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
