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
