from math import atan2
from qiskit import QuantumCircuit
from qiskit_aer import Aer

def apply_one_qubit(c):
  circ = QuantumCircuit(1)
  if abs(c[1][0]) > 1E-10 and abs(c[1][0] - c[0][1]) < 1E-10 or \
     abs(c[0][0]) > 1E-10 and abs(c[0][0] - c[1][1]) > 1E-10:
    circ.z(0)
  theta = atan2(c[1][0], c[0][0])
  circ.ry(2 * theta, 0)
  return circ.to_gate()

coef = [[1, 0], [0, 1]]
coef = [[1, 0], [0, -1]]
coef = [[0, 1], [1, 0]]
coef = [[0, -1], [1, 0]]
coef = [[0.6, -0.8], [0.8, 0.6]]
coef = [[0.6, 0.8], [0.8, -0.6]]
coef = [[-0.6, 0.8], [0.8, 0.6]]

circ = QuantumCircuit(1)
circ.append(apply_one_qubit(coef), [0])
circ = circ.decompose()

simulator = Aer.get_backend('unitary_simulator')
res = simulator.run(circ).result()
matrix = res.get_unitary().data
print(matrix)
