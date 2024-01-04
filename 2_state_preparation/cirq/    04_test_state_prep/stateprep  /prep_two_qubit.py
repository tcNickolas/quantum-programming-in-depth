import numpy as np
import cirq 

def prep_two_qubit(a):
    b0 = np.sqrt(a[0]**2 + a[2]**2)
    b1 = np.sqrt(a[1]**2 + a[3]**2)
    
    theta1 = np.arctan2(b1, b0)
    theta2 = np.arctan2(a[3], a[1])
    theta3 = np.arctan2(a[2], a[0])

    qc = cirq.Circuit()

    # Append the gate for the first qubit
    qc += cirq.ry(2 * theta1)(cirq.LineQubit(0))

    # Append the controlled gates for the second qubit
    controlled_prep_a1_a3 = cirq.ControlledGate(cirq.ry(2 * theta2))
    qc += controlled_prep_a1_a3.on(cirq.LineQubit(0), cirq.LineQubit(1))

    controlled_prep_a0_a2 = cirq.ControlledGate(cirq.ry(2 * theta3), control_values=[0])
    qc += controlled_prep_a0_a2.on(cirq.LineQubit(0), cirq.LineQubit(1))

    return qc

