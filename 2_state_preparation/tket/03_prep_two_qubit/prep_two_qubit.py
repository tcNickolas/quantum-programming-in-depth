from math import atan2, sqrt, pi
from pytket.circuit import Circuit, CircBox, QControlBox
from pytket.extensions.qiskit import AerStateBackend

backend = AerStateBackend()

def prep_one_qubit(alpha, beta):
    circ = Circuit(1)
    theta = atan2(beta, alpha)
    circ.Ry(2 * (theta / pi), 0)
    circ_gate = CircBox(circ)
    return circ_gate

def prep_two_qubit(a):
    b0 = sqrt(a[0]**2 + a[2]**2)
    b1 = sqrt(a[1]**2 + a[3]**2)
    circ = Circuit(2)
    # the control qubit is qubit 1, as the indexing is big-endian
    circ.add_circbox(prep_one_qubit(b0, b1), [1])

    controlled_one_qubit_prep_0 = QControlBox(prep_one_qubit(a[1], a[3]), n_controls=1)
    circ.add_qcontrolbox(controlled_one_qubit_prep_0, [1, 0])

    controlled_one_qubit_prep_1 = QControlBox(prep_one_qubit(a[0], a[2]), n_controls=1, control_state=0)
    circ.add_qcontrolbox(controlled_one_qubit_prep_1, [1, 0])

    return circ

def prep_two_qubit_demo(a):
    circ = prep_two_qubit(a)      #not decomposed into simpler gates
    circ.get_statevector()

    compiled_circ = backend.get_compiled_circuit(circ)
    state_vector = backend.run_circuit(compiled_circ).get_state()
    print(state_vector.round(5))

prep_two_qubit_demo([0.36, 0.48, 0.64, -0.48])
