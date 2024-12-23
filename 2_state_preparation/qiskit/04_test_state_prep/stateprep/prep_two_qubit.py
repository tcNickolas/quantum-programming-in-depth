from math import atan2, sqrt
from qiskit import QuantumCircuit

def pre_one_qubit(alpha, beta):
    circ = QuantumCircuit(1, name=f'Prep({alpha}, {beta})')
    theta = atan2(beta, alpha)
    circ.ry(2 * theta, 0)
    # print(circuit.draw())
    return circ.to_gate()

def prep_two_qubit(a):
    b0 = sqrt(a[0]**2 + a[2]**2)
    b1 = sqrt(a[1]**2 + a[3]**2)

    circ = QuantumCircuit(2)
    circ.append(pre_one_qubit(b0, b1), [0])

    circ.append(pre_one_qubit(a[1], a[3]).control(1), [0, 1])

    circ.append(pre_one_qubit(a[0], a[2]).control(1, ctrl_state=0), [0, 1])

    return circ
