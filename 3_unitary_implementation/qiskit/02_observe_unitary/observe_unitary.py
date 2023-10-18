from math import atan2
from pytest import approx
from qiskit import QuantumCircuit
from qiskit_aer import Aer

def apply_one_qubit(u):
  circ = QuantumCircuit(1)
  if u[0][0] == approx(-u[1][1]) and \
     u[1][0] == approx(u[0][1]):
    circ.z(0)
  theta = atan2(u[1][0], u[0][0])
  circ.ry(2 * theta, 0)
  return circ.to_gate()

coef = [[0.6, -0.8], [0.8, 0.6]]

circ = QuantumCircuit(1)
circ.append(apply_one_qubit(coef), [0])
circ = circ.decompose()

simulator = Aer.get_backend('unitary_simulator')
res = simulator.run(circ).result()
matrix = res.get_unitary().data
print(matrix)
