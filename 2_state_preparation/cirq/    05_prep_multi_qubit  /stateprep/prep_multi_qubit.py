# this code has issues, not sure how to construct gate from circuit in cirq
import numpy as np
import cirq

def prep_multi_qubit(n, a):
    qc = cirq.Circuit()

    if n == 1:
        qc += cirq.ry(2 * np.arctan2(a[0], a[1]))(cirq.LineQubit(0))
        return qc

    zero_amps = a[0::2]
    one_amps = a[1::2]

    m0 = np.sqrt(sum(alpha**2 for alpha in zero_amps))
    m1 = np.sqrt(sum(beta**2 for beta in one_amps))
    


    qc += cirq.ry(2 * np.arctan2(m0, m1))(cirq.LineQubit(0))

    target_qubits = [cirq.LineQubit(i) for i in range(1, n)]
    
    qc += cirq.ControlledGate(prep_multi_qubit(n - 1, zero_amps), control_values=[0]).on(cirq.LineQubit(0), *target_qubits)
    qc += cirq.ControlledGate(prep_multi_qubit(n - 1, one_amps)).on(cirq.LineQubit(0), *target_qubits)

    return qc
