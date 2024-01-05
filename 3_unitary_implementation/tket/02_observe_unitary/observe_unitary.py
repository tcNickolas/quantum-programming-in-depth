from math import atan2, isclose, pi
from pytket.circuit import Circuit, CircBox
from pytket.extensions.qiskit import AerUnitaryBackend

def apply_one_qubit(u):
  circ = Circuit(1)
  if isclose(u[0][0], -u[1][1]) and isclose(u[1][0], u[0][1]):
    circ.Z(0)
  theta = atan2(u[1][0], u[0][0])
  circ.Ry(2 * (theta/pi), 0)
  circ_gate = CircBox(circ)
  return circ_gate

coef = [[0.6, -0.8], [0.8, 0.6]]

circ = Circuit(1)
circ.add_circbox(apply_one_qubit(coef), [0])
backend = AerUnitaryBackend()
compiled_circ = backend.get_compiled_circuit(circ)
result = backend.run_circuit(compiled_circ)
unitary = result.get_unitary()
matrix = unitary.real
print(matrix)
