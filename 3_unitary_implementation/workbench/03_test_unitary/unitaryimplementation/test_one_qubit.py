from math import cos, pi, sin
from random import randint, random
from psiqworkbench import QPU, Qubits
from .one_qubit_unitary import ApplyOneQubitUnitary
import pytest

@pytest.mark.parametrize("u",
    [ [[1.0, 0.0], [0.0, 1.0]],
      [[1.0, 0.0], [0.0, -1.0]],
      [[-1.0, 0.0], [0.0, 1.0]],
      [[-1.0, 0.0], [0.0, -1.0]],
      [[0.0, 1.0], [1.0, 0.0]],
      [[0.0, 1.0], [-1.0, 0.0]],
      [[0.0, -1.0], [1.0, 0.0]],
      [[0.0, -1.0], [-1.0, 0.0]] ])
def test_apply_one_qubit(u):
    qpu = QPU(num_qubits=1, filters=">>unitary>>")
    reg = Qubits(1, "reg", qpu)

    apply_unitary = ApplyOneQubitUnitary()
    apply_unitary.compute(reg, u)

    ufilter = qpu.get_filter_by_name('>>unitary>>')
    matrix = ufilter.get()
    for actual, expected in zip(matrix, u):
        assert actual == pytest.approx(expected)


def random_one_qubit_unitary():
    theta = random() * 2 * pi
    sign = +1 if randint(0, 1) == 1 else -1
    return [[cos(theta), sign * sin(theta)], 
            [-sin(theta), sign * cos(theta)]]


def test_dense():
    for _ in range(1, 20):
        test_apply_one_qubit(random_one_qubit_unitary())