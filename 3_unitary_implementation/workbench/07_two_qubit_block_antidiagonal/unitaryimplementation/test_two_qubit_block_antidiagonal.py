from math import cos, pi, sin
from random import randint, random
from psiqworkbench import QPU, Qubits
from .two_qubit_block_antidiagonal import ApplyTwoQubitBlockAntiDiagonal
import pytest

def run_test_apply_two_qubit_block_antidiagonal(a, b):
    qpu = QPU(num_qubits=2, filters=">>unitary>>")
    reg = Qubits(2, "reg", qpu)

    apply_unitary = ApplyTwoQubitBlockAntiDiagonal()
    apply_unitary.compute(reg, a, b)

    ufilter = qpu.get_filter_by_name('>>unitary>>')
    matrix = ufilter.get()

    complete_coef = [
        [0., 0.] + a[0],
        [0., 0.] + a[1],
        b[0] + [0., 0.],
        b[1] + [0., 0.]]
                  
    for actual, expected in zip(matrix, complete_coef):
        assert actual == pytest.approx(expected)


def random_one_qubit_unitary():
    theta = random() * 2 * pi
    sign = +1 if randint(0, 1) == 1 else -1
    return [[cos(theta), sign * sin(theta)], 
            [-sin(theta), sign * cos(theta)]]


def test_apply_block_antidiagonal():
    for _ in range(1, 20):
        a = random_one_qubit_unitary()
        b = random_one_qubit_unitary()
        run_test_apply_two_qubit_block_antidiagonal(a, b)
