from math import atan2, sqrt
from qiskit import QuantumCircuit
from typing import List

def pre_one_qubit(alpha: float, beta: float):
    circuit = QuantumCircuit(1, name=f'Prep({alpha}, {beta})')
    theta = atan2(beta, alpha)
    circuit.ry(2 * theta, 0)
    # print(circuit.draw())
    return circuit.to_gate()

def prep_two_qubit(a: List[float]):
    b0 = sqrt(a[0]**2 + a[2]**2)
    b1 = sqrt(a[1]**2 + a[3]**2)

    circuit = QuantumCircuit(2)
    circuit.append(pre_one_qubit(b0, b1), [0])

    circuit.append(pre_one_qubit(a[1], a[3]).control(1), [0, 1])

    circuit.append(pre_one_qubit(a[0], a[2]).control(1, ctrl_state=0), [0, 1])

    # print(circuit.draw())

    return circuit
