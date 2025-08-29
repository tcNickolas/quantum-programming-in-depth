from math import sqrt
from random import randint, uniform
from psiqworkbench import QPU, Qubits
from .prep_multi_qubit import StatePrep
import pytest

def run_test_prep_multiqubit(n: int, amps: list[float]) -> None:
    qpu = QPU(num_qubits=n + (n - 2 if n > 2 else 0))
    reg = Qubits(n, "reg", qpu)

    state_prep = StatePrep()
    state_prep.compute(reg, amps)

    state_vector = qpu.pull_state()[0 : 2 ** n]
    assert state_vector == pytest.approx(amps)


@pytest.mark.parametrize("amps",
    [ [1, 0],
      [0, 1],
      [-1, 0],
      [0, -1],
      [0.6, 0.8],
      [0.6, -0.8],
      [-0.6, 0.8],
      [-0.6, -0.8]
    ])
def test_prep_one_qubit(amps: list[float]):
    run_test_prep_multiqubit(1, amps)


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
def test_prep_two_qubit(amps: list[float]):
    run_test_prep_multiqubit(2, amps)


def test_random_unequal_superpositions():
    for _ in range(30):
        n = randint(2, 6)
        a = [uniform(-1.0, 1.0) for _ in range(2 ** n)]
        norm = sqrt(sum(a*a for a in a))
        a_norm = [j / norm for j in a]
        run_test_prep_multiqubit(n, a_norm)
