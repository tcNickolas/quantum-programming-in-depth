from math import atan2, isclose, pi
from pytket.circuit import Circuit, CircBox

def apply_one_qubit(u):
  circ = Circuit(1)
  if isclose(u[0][0], -u[1][1]) and isclose(u[1][0], u[0][1]):
    circ.Z(0)
  theta = atan2(u[1][0], u[0][0])
  circ.Ry(2 * (theta/pi), 0)
  circ_gate = CircBox(circ)
  return circ_gate
