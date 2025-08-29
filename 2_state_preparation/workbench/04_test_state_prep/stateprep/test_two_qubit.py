from math import sqrt
from psiqworkbench import QPU, Qubits
from .prep_two_qubit import prep_two_qubit
import pytest

@pytest.mark.parametrize("amps",
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
def test_prep_two_qubit(amps):
    qpu = QPU(num_qubits=2)
    reg = Qubits(2, "reg", qpu)
    prep_two_qubit(reg, amps)
    state_vector = qpu.pull_state()
    assert state_vector == pytest.approx(amps)