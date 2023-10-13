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
