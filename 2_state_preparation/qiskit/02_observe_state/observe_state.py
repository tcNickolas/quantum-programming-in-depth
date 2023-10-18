from math import atan2
from qiskit import QuantumCircuit
from qiskit_aer import Aer

simulator = Aer.get_backend('aer_simulator')

alpha, beta = 0.6, 0.8

circ = QuantumCircuit(1)
theta = atan2(beta, alpha)
circ.ry(2 * theta, 0)
circ.save_statevector()

res = simulator.run(circ).result()
state_vector = res.get_statevector()
print(state_vector)
