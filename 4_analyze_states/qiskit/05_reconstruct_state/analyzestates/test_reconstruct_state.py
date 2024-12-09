from math import atan2, cos, pi, sin
from random import randrange, uniform
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from .reconstruct_state import reconstruct_state

def prep_state(alpha, beta):
  circ = QuantumCircuit(1)
  circ.ry(2. * atan2(beta, alpha), 0)
  return circ

def test_reconstruct_state():
  for _ in range(10):
    angle = uniform(0, pi / 2)
    alpha = cos(angle)
    beta = (1 if randrange(2) == 0 else -1) * sin(angle)

    (alpha_res, beta_res) = reconstruct_state(prep_state(alpha, beta))

    print(f"Actual amplitudes {alpha},{beta}, returned {alpha_res},{beta_res}")
    assert abs(alpha - alpha_res) < 0.1 and abs(beta - beta_res) < 0.1
