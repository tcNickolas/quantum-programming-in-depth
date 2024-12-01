from math import atan2, sqrt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

simulator = Aer.get_backend('aer_simulator')

def prep_one_qubit(alpha, beta):
    circ = QuantumCircuit(1, name=f'Prep({alpha}, {beta})')
    theta = atan2(beta, alpha)
    circ.ry(2 * theta, 0)
    return circ.to_gate()

def prep_two_qubit(a):
    b0 = sqrt(a[0]**2 + a[2]**2)
    b1 = sqrt(a[1]**2 + a[3]**2)

    circ = QuantumCircuit(2)
    circ.append(prep_one_qubit(b0, b1), [0])

    circ.append(prep_one_qubit(a[1], a[3]).control(1), [0, 1])

    circ.append(prep_one_qubit(a[0], a[2]).control(1, ctrl_state=0), [0, 1])

    return circ

def prep_two_qubit_demo(a):
    circ = prep_two_qubit(a)
    circ.save_statevector()

    circ = transpile(circ, backend=simulator)
    res = simulator.run(circ).result()
    state_vector = res.get_statevector()
    print([d.round(5) for d in state_vector.data])

prep_two_qubit_demo([0.36, 0.48, 0.64, -0.48])
