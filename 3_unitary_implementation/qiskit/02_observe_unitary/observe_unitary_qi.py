from math import atan2, isclose
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

def apply_one_qubit(u):
  circ = QuantumCircuit(1)
  if isclose(u[0][0], -u[1][1]) and \
     isclose(u[1][0], u[0][1]):
    circ.z(0)
  theta = atan2(u[1][0], u[0][0])
  circ.ry(2 * theta, 0)
  return circ.to_gate()

coef = [[0.6, -0.8], [0.8, 0.6]]

op = Operator(apply_one_qubit(coef))
print(op.data)
