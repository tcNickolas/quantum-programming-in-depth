from math import atan2
from qiskit import QuantumCircuit

alpha, beta = 0.6, 0.8

circ = QuantumCircuit(1)
theta = 2 * atan2(beta, alpha)
circ.ry(theta, 0)
