from pytest import approx
from math import atan2, isclose, pi, ceil, log2
from pytket.circuit import Circuit, CircBox, QControlBox

def apply_one_qubit(u):
    circ = Circuit(1)
    if isclose(u[0][0], -u[1][1]) and isclose(u[1][0], u[0][1]):
        circ.Z(0)
    theta = atan2(u[1][0], u[0][0])
    circ.Ry(2 * (theta/pi), 0)
    circ_gate = CircBox(circ)
    return circ_gate

def apply_two_qubit_cs_matrix(c0, s0, c1, s1):
  circ = Circuit(2)
  m0 = [[c0, -s0], [s0, c0]]
  m1 = [[c1, -s1], [s1, c1]]
  control_1 = QControlBox(apply_one_qubit(m1), n_controls=1)
  control_0 = QControlBox(apply_one_qubit(m0), n_controls=1, control_state=0)
  circ.add_qcontrolbox(control_1, [1, 0])
  circ.add_qcontrolbox(control_0, [1, 0])
  circ_gate = CircBox(circ)
  return circ_gate

def apply_arbitrary_cs_matrix(n, cs):
  circ = Circuit(n)
  for (k, (c, s)) in enumerate(cs):
    m = [[c, -s], [s, c]]
    # two_power = 2**(n-1)
    # l = two_power - k 
    control = QControlBox(apply_one_qubit(m), n_controls=n-1, control_state=k)
    circ.add_qcontrolbox(control, list(range(1, n)) + [0])
  circ_gate = CircBox(circ)
  return circ_gate