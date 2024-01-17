from math import atan2, sqrt, pi
from pytket.circuit import Circuit, CircBox, QControlBox
from pytest import approx
from pytket.extensions.qiskit import AerStateBackend

backend = AerStateBackend()
def prep_one_qubit(alpha, beta):
    circ = Circuit(1)
    theta = atan2(beta, alpha)
    circ.Ry(2 * (theta / pi), 0)
    circ_gate = CircBox(circ)
    return circ_gate

def prep_multi_qubit(n, a):
    circ = Circuit(n)
    if n == 1:
        circ.add_circbox(prep_one_qubit(a[0], a[1]), [0])
        return circ

    zero_amps = a[0::2]
    one_amps = a[1::2]

    m0 = sqrt(sum(a*a for a in zero_amps))
    m1 = sqrt(sum(a*a for a in one_amps))

    circ.add_circbox(prep_one_qubit(m0, m1), [n-1])

    circ_zero_amps = CircBox(prep_multi_qubit(n-1, zero_amps))
    circ_one_amps = CircBox(prep_multi_qubit(n-1, one_amps))

    controlled_multi_qubit_prep_0 = QControlBox(circ_zero_amps, n_controls=1, control_state=0)
    controlled_multi_qubit_prep_1 = QControlBox(circ_one_amps, n_controls=1, control_state=1)

    # the controls in the qcontrolbox occupy the low-index ports of the resulting operation
    circ.add_qcontrolbox(controlled_multi_qubit_prep_0, [n-1] + list(range(0, n-1)))
    circ.add_qcontrolbox(controlled_multi_qubit_prep_1, [n-1] + list(range(0, n-1)))
    return circ

def run_test_prep_multi_qubit(n, a):
  assert len(a) == 2 ** n
  circ = prep_multi_qubit(n, a)
  circ.get_statevector()

  compiled_circ = backend.get_compiled_circuit(circ)
  state_vector = backend.run_circuit(compiled_circ).get_state()
  assert state_vector == approx(a)
  print(state_vector)

def test_basis_states():
    n = 3
    a = [0.] * 2 ** n
    a[2] = 1.
    run_test_prep_multi_qubit(n, a)

