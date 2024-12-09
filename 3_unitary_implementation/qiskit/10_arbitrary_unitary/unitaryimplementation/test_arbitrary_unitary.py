from numpy import identity, matmul, matrix
from numpy.random import default_rng
from qiskit.quantum_info import Operator
from scipy.linalg import qr
from pytest import approx
from .arbitrary_unitary import apply_arbitrary_unitary

def run_test_apply_arbitrary_unitary(n, u):
  op = Operator(apply_arbitrary_unitary(n, u))
  matrix = op.data

  for actual, expected in zip(matrix, u):
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
