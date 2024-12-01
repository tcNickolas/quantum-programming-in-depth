from .prep_two_qubit import prep_two_qubit
import pytest
from math import sqrt
from qiskit import transpile
from qiskit_aer import Aer

simulator = Aer.get_backend('aer_simulator')

@pytest.mark.parametrize("a",
    [ [1., 0., 0., 0.],
      [0., 1., 0., 0.],
      [0., 0., 1., 0.],
      [0., 0., 0., 1.],
      [0.5, 0.5, 0.5, 0.5],
      [-0.5, 0.5, 0.5, -0.5],
      [0.5, -0.5, 0.5, 0.5],
      [0.5, 0.5, -0.5, 0.5],
      [0.5, 0.5, 0.5, -0.5],
      [1. / sqrt(2.), 0., 0., 1. / sqrt(2.)],
      [1. / sqrt(2.), 0., 0., -1. / sqrt(2.)],
      [0., 1. / sqrt(2.), 1. / sqrt(2.), 0.],
      [0., 1. / sqrt(2.), -1. / sqrt(2.), 0.],
      [0.36, 0.48, 0.64, -0.48],
      [1. / sqrt(3.), -1. / sqrt(3.), 1. / sqrt(3.), 0.]
    ])
def test_prep_two_qubit(a):
  circ = prep_two_qubit(a)
  circ.save_statevector()

  circ = transpile(circ, backend=simulator)
  res = simulator.run(circ).result()
  state_vector = res.get_statevector().data

  assert state_vector == pytest.approx(a)
