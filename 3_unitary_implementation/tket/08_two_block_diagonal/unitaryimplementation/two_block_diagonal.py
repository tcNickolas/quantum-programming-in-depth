from math import atan2, isclose, pi
from pytket.circuit import Circuit, CircBox, QControlBox

def apply_one_qubit(u):
    circ = Circuit(1)
    if isclose(u[0][0], -u[1][1]) and isclose(u[1][0], u[0][1]):
        circ.Z(0)
    theta = atan2(u[1][0], u[0][0])
    circ.Ry(2 * (theta/pi), 0)
    circ_gate = CircBox(circ)
    return circ_gate

def apply_two_qubit_block_diagonal(a, b):
    circ = Circuit(2)
    control_1 = QControlBox(apply_one_qubit(b), n_controls=1, control_state=1)
    control_0 = QControlBox(apply_one_qubit(a), n_controls=1, control_state=0)
    circ.add_qcontrolbox(control_1, [0, 1])
    circ.add_qcontrolbox(control_0, [0, 1])
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

def apply_two_qubit_block_antidiagonal(a, b):
    circ = Circuit(2)
    id = [[1., 0.], [0., 1.]]
    minus_a = [[-a[0][0], -a[0][1]], [-a[1][0], -a[1][1]]]
    circ.add_circbox(apply_two_qubit_block_diagonal(id, minus_a), [0, 1])
    circ.add_circbox(apply_two_qubit_cs_matrix(*(0., 1.), *(0., 1.)), [0, 1])
    circ.add_circbox(apply_two_qubit_block_diagonal(id, b), [0, 1])
    circ_gate = CircBox(circ)
    return circ_gate

def apply_arbitrary_unitary(n, u):
  # We cannot implement this completely yet,
  # but we can implement some special cases.
  if n == 1:
    return apply_one_qubit(u)
  if n == 2:
    if all(isclose(v, 0) for v in
           u[0][2:4] + u[1][2:4] +
           u[2][0:2] + u[3][0:2]):
      # Block-diagonal matrix.
      tl = [u[0][0:2], u[1][0:2]]
      br = [u[2][2:4], u[3][2:4]]
      return apply_two_qubit_block_diagonal(tl, br)
    if all(isclose(v, 0) for v in
           u[0][0:2] + u[1][0:2] +
           u[2][2:4] + u[3][2:4]):
      # Block-anti-diagonal matrix.
      tr = [u[0][2:4], u[1][2:4]]
      bl = [u[2][0:2], u[3][0:2]]
      return apply_two_qubit_block_antidiagonal(tr, bl)
    raise NotImplementedError("The case of " +
      "arbitrary 2-qubit unitaries is not implemented yet")
  raise NotImplementedError(
    "The case of 3+-qubit unitaries is not implemented yet")

def apply_two_block_diagonal(n, a, b):
  circ = Circuit(n)
  control_1 = QControlBox(apply_arbitrary_unitary(n-1, b), n_controls=1)
  control_0 = QControlBox(apply_arbitrary_unitary(n-1, a), n_controls=1, control_state=0)
  circ.add_qcontrolbox(control_1, [0] + list(range(1, n)))
  circ.add_qcontrolbox(control_0, [0] + list(range(1, n)))
  circ_gate = CircBox(circ)
  return circ_gate
  return circ
