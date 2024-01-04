from math import atan2
import cirq

alpha, beta = 0.6, 0.8
theta = atan2(beta, alpha)

qc = cirq.Circuit()
qc.append(cirq.Ry(rads=2 * theta)(*cirq.LineQubit.range(1)))
simulator = cirq.Simulator()
res = simulator.simulate(qc)

state_vector = res.final_state_vector
print(state_vector)
