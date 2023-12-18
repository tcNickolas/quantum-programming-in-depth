from two_qubit import *
from math import sqrt
from pytest import approx
from pytket.extensions.qiskit import AerStateBackend

backend = AerStateBackend()

def run_test_prep_two_qubit(a):
    circ = prep_two_qubit(a)      #not decomposed into simpler gates
    circ.get_statevector()

    compiled_circ = backend.get_compiled_circuit(circ)
    state_vector = backend.run_circuit(compiled_circ).get_state()

    for actual, expected in zip(state_vector, a):
        assert actual == approx(expected)

def test_basis_states():
    run_test_prep_two_qubit([1., 0., 0., 0.])
    run_test_prep_two_qubit([0., 1., 0., 0.])
    run_test_prep_two_qubit([0., 0., 1., 0.])
    run_test_prep_two_qubit([0., 0., 0., 1.])


def test_equal_superpositions():
    run_test_prep_two_qubit([0.5, 0.5, 0.5, 0.5])
    run_test_prep_two_qubit([-0.5, 0.5, 0.5, -0.5])
    run_test_prep_two_qubit([0.5, -0.5, 0.5, 0.5])
    run_test_prep_two_qubit([0.5, 0.5, -0.5, 0.5])
    run_test_prep_two_qubit([0.5, 0.5, 0.5, -0.5])

def test_bell_states():
    run_test_prep_two_qubit([1. / sqrt(2.), 0., 0., 1. / sqrt(2.)])
    run_test_prep_two_qubit([1. / sqrt(2.), 0., 0., -1. / sqrt(2.)])
    run_test_prep_two_qubit([0., 1. / sqrt(2.), 1. / sqrt(2.), 0.])
    run_test_prep_two_qubit([0., 1. / sqrt(2.), -1. / sqrt(2.), 0.])

def test_unequal_superpositions():
    run_test_prep_two_qubit([0.36, 0.48, 0.64, -0.48])
    run_test_prep_two_qubit([1. / sqrt(3.), -1. / sqrt(3.), 1. / sqrt(3.), 0.])
