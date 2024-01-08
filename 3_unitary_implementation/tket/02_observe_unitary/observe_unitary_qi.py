from math import atan2, isclose, pi
from pytket.circuit import Circuit

def apply_one_qubit(u):
  circ = Circuit(1)
  if isclose(u[0][0], -u[1][1]) and isclose(u[1][0], u[0][1]):
    circ.z(0)
  theta = atan2(u[1][0], u[0][0])
  circ.Ry(2 * (theta/pi), 0)
  return circ

coef = [[0.6, -0.8], [0.8, 0.6]]

op = apply_one_qubit(coef).get_unitary()
print(op)
