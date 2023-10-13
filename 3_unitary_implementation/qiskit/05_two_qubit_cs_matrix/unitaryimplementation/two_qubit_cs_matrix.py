from math import atan2
from qiskit import QuantumCircuit

def apply_one_qubit(c):
  circ = QuantumCircuit(1)
  if abs(c[1][0]) > 1E-10 and abs(c[1][0] - c[0][1]) < 1E-10 or \
     abs(c[0][0]) > 1E-10 and abs(c[0][0] - c[1][1]) > 1E-10:
    circ.z(0)
  theta = atan2(c[1][0], c[0][0])
  circ.ry(2 * theta, 0)
  return circ.to_gate()

def apply_two_qubit_cs_matrix(c0, s0, c1, s1):
  circ = QuantumCircuit(2)
  m0 = [[c0, -s0], [s0, c0]]
  m1 = [[c1, -s1], [s1, c1]]
  circ.append(apply_one_qubit(m1).control(1), [0, 1])
  circ.append(apply_one_qubit(m0).control(1, ctrl_state=0), [0, 1])  
  return circ
