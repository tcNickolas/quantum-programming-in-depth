from pytest import approx
from .phase_estimation import *
from .test_inputs import *

def test_one_bit_phase_estimation():
  for ind in [0, 1]:
    for _ in range(50):
      est_phase = one_bit_phase_estimation(1, z_eigenvectors[ind], z_gate())
      assert est_phase == approx(z_eigenphases[ind])


def test_iterative_phase_estimation():
  for (n_qubits, n_eigenvectors, unitary, eigenvectors, eigenphases) in [
    (1, 2, z_gate(), z_eigenvectors, z_eigenphases),
    (2, 3, inc_gate(), inc_eigenvectors, inc_eigenphases),
    (1, 2, t_gate(), z_eigenvectors, t_eigenphases)
  ]:
    for ind in range(n_eigenvectors):
      for _ in range(10):
        est_phase = iterative_phase_estimation(n_qubits, eigenvectors[ind], unitary)
        assert est_phase == approx(eigenphases[ind], abs=0.01)


def test_adaptive_phase_estimation():
  for (n_qubits, n_eigenvectors, unitary, eigenvectors, eigenphases) in [
    (1, 2, z_gate(), z_eigenvectors, z_eigenphases),
    (2, 4, inc_gate(), inc_eigenvectors, inc_eigenphases)
  ]:
    for ind in range(n_eigenvectors):
      for _ in range(10):
        est_phase = two_bit_adaptive_phase_estimation(n_qubits, eigenvectors[ind], unitary)
        assert est_phase == approx(eigenphases[ind])


def test_quantum_phase_estimation():
  for (n_qubits, n_eigenvectors, unitary, eigenvectors, eigenphases) in [
    (1, 2, z_gate(), z_eigenvectors, z_eigenphases),
    (2, 4, inc_gate(), inc_eigenvectors, inc_eigenphases)
  ]:
    for ind in range(n_eigenvectors):
      for _ in range(10):
        est_phase = two_bit_quantum_phase_estimation(n_qubits, eigenvectors[ind], unitary)
        assert est_phase == approx(eigenphases[ind])
