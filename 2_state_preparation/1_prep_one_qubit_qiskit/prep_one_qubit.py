from math import atan2
from qiskit import QuantumCircuit

alpha, beta = 0.6, 0.8

circuit = QuantumCircuit(1)
theta = atan2(beta, alpha)
circuit.ry(2 * theta, 0)
