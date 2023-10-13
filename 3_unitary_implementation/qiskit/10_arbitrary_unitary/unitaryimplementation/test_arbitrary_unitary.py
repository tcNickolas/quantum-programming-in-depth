from .arbitrary_unitary import apply_arbitrary_unitary
from math import pi, cos, sin
from numpy import identity, matrix, matmul
from numpy.random import default_rng
from pytest import approx
from scipy.linalg import qr
from random import random, randint
from qiskit import QuantumCircuit
from qiskit_aer import Aer

def run_test_apply_arbitrary_unitary(n, u):
  circ = QuantumCircuit(n)
  circ.append(apply_arbitrary_unitary(n, u), range(n))
  circ = circ.decompose(reps=n+2)

  simulator = Aer.get_backend('unitary_simulator')
  res = simulator.run(circ).result()
  matrix = res.get_unitary().data

  for actual, expected in zip(u, matrix):
    assert actual == approx(expected)

def test_apply_arbitrary_unitary():
  rng = default_rng()
  for n in range(1, 5):
    for _ in range(10):
      t = rng.standard_normal((2**n, 2**n))
      u, _ = qr(t)
      # Double-check that u is unitary
      assert matmul(u, matrix.transpose(u)) == approx(identity(2**n))
      run_test_apply_arbitrary_unitary(n, u)
