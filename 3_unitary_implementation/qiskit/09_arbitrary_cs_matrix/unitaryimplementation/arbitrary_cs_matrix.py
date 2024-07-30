from math import atan2, isclose
from qiskit import QuantumCircuit

def apply_one_qubit(u):
  circ = QuantumCircuit(1)
  if isclose(u[0][0], -u[1][1]) and isclose(u[1][0], u[0][1]):
    circ.z(0)
  theta = atan2(u[1][0], u[0][0])
  circ.ry(2 * theta, 0)
  return circ.to_gate()

def apply_arbitrary_cs_matrix(n, cs):
  circ = QuantumCircuit(n)
  for (k, (c, s)) in enumerate(cs):
    m = [[c, -s], [s, c]]
    circ.append(apply_one_qubit(m).control(n - 1, ctrl_state=k), range(n))
  return circ
