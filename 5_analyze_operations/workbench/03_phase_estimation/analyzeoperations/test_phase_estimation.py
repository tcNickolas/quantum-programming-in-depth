from cmath import exp, pi, isclose
from psiqworkbench import QPU, Qubits
from .phase_estimation import *
import pytest

# Unitaries and eigenvectors that act as inputs to phase estimation algorithms

def z_gate(q, cond=0):
    q.z(cond=cond)

def inc_gate(qs, cond=0):
    '''Two-qubit incrementer gate'''
    qs[1].x(cond=qs[0] | cond)
    qs[0].x(cond=cond)

def t_gate(q, cond=0):
    q.t(cond=cond)

zt_eigenvectors = [[1, 0], [0, 1]]

inc_eigenvectors = [
    [0.5, 0.5, 0.5, 0.5],
    [0.5, -0.5, 0.5, -0.5],
    [0.5, -0.5j, -0.5, 0.5j],
    [0.5, 0.5j, -0.5, -0.5j]
  ]

z_eigenphases = [0, 0.5]

inc_eigenphases = [0.0, 0.5, 0.25, 0.75]

t_eigenphases = [0, 0.125]


# --------------------------------------- Tests ---------------------------------------

@pytest.mark.parametrize("n_qubits, n_eigenvectors, unitary, eigenvectors, eigenphases",
    [
        (1, 2, z_gate, zt_eigenvectors, z_eigenphases),
        (2, 4, inc_gate, inc_eigenvectors, inc_eigenphases),
        (1, 2, t_gate, zt_eigenvectors, t_eigenphases)
    ])
def test_validate_inputs(n_qubits, n_eigenvectors, unitary, eigenvectors, eigenphases):
    qpu = QPU()
    for ind in range(n_eigenvectors):
        qpu.reset(n_qubits)
        qs = Qubits(n_qubits, "qs", qpu)
        qs.push_state(eigenvectors[ind])
        unitary(qs)
        state_vector = qpu.pull_state()

        exp_vector = [amp * exp(2 * 1j * pi * eigenphases[ind]) for amp in eigenvectors[ind]]
        for (actual, expected) in zip(state_vector, exp_vector):
            assert isclose(actual, expected)
            

def test_one_bit_phase_estimation():
    for ind in [0, 1]:
        for _ in range(50):
            est_phase = one_bit_phase_estimation(1, zt_eigenvectors[ind], z_gate)
            assert est_phase == pytest.approx(z_eigenphases[ind])


@pytest.mark.parametrize("n_qubits, n_eigenvectors, unitary, eigenvectors, eigenphases",
    [
        (1, 2, z_gate, zt_eigenvectors, z_eigenphases),
        (2, 3, inc_gate, inc_eigenvectors, inc_eigenphases), # Don't test the 0.75 eigenphase, the algorithm won't work for it
        (1, 2, t_gate, zt_eigenvectors, t_eigenphases)
    ])
def test_iterative_phase_estimation(n_qubits, n_eigenvectors, unitary, eigenvectors, eigenphases):
    for ind in range(n_eigenvectors):   
        for _ in range(10):
            est_phase = iterative_phase_estimation(n_qubits, eigenvectors[ind], unitary)
            assert est_phase == pytest.approx(eigenphases[ind], abs=0.01)


@pytest.mark.parametrize("n_qubits, n_eigenvectors, unitary, eigenvectors, eigenphases",
    [
        (1, 2, z_gate, zt_eigenvectors, z_eigenphases),
        (2, 4, inc_gate, inc_eigenvectors, inc_eigenphases)
    ])
def test_adaptive_phase_estimation(n_qubits, n_eigenvectors, unitary, eigenvectors, eigenphases):
    for ind in range(n_eigenvectors):   
        for _ in range(10):
            est_phase = two_bit_adaptive_phase_estimation(n_qubits, eigenvectors[ind], unitary)
            assert est_phase == pytest.approx(eigenphases[ind], abs=0.01)


@pytest.mark.parametrize("n_qubits, n_eigenvectors, unitary, eigenvectors, eigenphases",
    [
        (1, 2, z_gate, zt_eigenvectors, z_eigenphases),
        (2, 4, inc_gate, inc_eigenvectors, inc_eigenphases)
    ])
def test_quantum_phase_estimation(n_qubits, n_eigenvectors, unitary, eigenvectors, eigenphases):
    for ind in range(n_eigenvectors):   
        for _ in range(10):
            est_phase = two_bit_quantum_phase_estimation(n_qubits, eigenvectors[ind], unitary)
            assert est_phase == pytest.approx(eigenphases[ind], abs=0.01)