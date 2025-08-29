from math import cos, pi, sin
from random import randint, random
from psiqworkbench import QPU, Qubits
from .two_qubit_cs_matrix import ApplyTwoQubitCSMatrix
import pytest

def run_test_apply_two_qubit_cs_matrix(c0, s0, c1, s1):
    qpu = QPU(num_qubits=2, filters=">>unitary>>")
    reg = Qubits(2, "reg", qpu)

    apply_unitary = ApplyTwoQubitCSMatrix()
    apply_unitary.compute(reg, c0, s0, c1, s1)

    ufilter = qpu.get_filter_by_name('>>unitary>>')
    matrix = ufilter.get()

    complete_coef = [
        [c0, 0., -s0, 0.],
        [0., c1, 0., -s1],
        [s0, 0., c0, 0.],
        [0., s1, 0., c1]]
                  
    for actual, expected in zip(matrix, complete_coef):
        assert actual == pytest.approx(expected)


def random_one_qubit_unitary():
    theta = random() * 2 * pi
    sign = +1 if randint(0, 1) == 1 else -1
    return [[cos(theta), sign * sin(theta)], 
            [-sin(theta), sign * cos(theta)]]


def test_two_qubit_cs_matrix():
    for _ in range(1, 20):
        m0 = random_one_qubit_unitary()
        m1 = random_one_qubit_unitary()
        run_test_apply_two_qubit_cs_matrix(m0[0][0], m0[1][0], m1[0][0], m1[1][0])
