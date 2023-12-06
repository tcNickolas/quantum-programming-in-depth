from math import atan2, pi
from qiskit import QuantumCircuit

def distinguish_zero_and_sup(alpha, beta):
  circ = QuantumCircuit(1, 1)
  # Figure out the angle of the line halfway between |0> and alpha |0> + beta |1>
  theta = atan2(beta, alpha) / 2
  circ.ry(- 2 * (theta - pi / 4), 0)
  circ.measure(0, 0)
  return circ
