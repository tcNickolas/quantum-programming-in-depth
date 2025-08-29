from math import atan2, cos, isclose, pi, sin
from random import randint, uniform
from functools import partial
from psiqworkbench import Qubits
from .reconstruct_unitary import *

def apply_one_qubit(reg: Qubits, u: list[list[float]]) -> None:
    if isclose(u[0][0], -u[1][1]) and isclose(u[1][0], u[0][1]):
        reg.z()
    theta = atan2(u[1][0], u[0][0])
    reg.ry(2 * theta * Units.rad)


def random_one_qubit_unitary():
    theta = uniform(0.1, pi / 2 - 0.1) * (1 if randint(0, 1) == 0 else -1)
    sign = +1 if randint(0, 1) == 1 else -1
    return [[cos(theta), -sign * sin(theta)], 
            [sin(theta), sign * cos(theta)]]


def test_reconstruct_unitary():
    for _ in range(50):
        matrix = random_one_qubit_unitary()
        unitary = partial(apply_one_qubit, u=matrix)

        matrix_res = reconstruct_unitary(unitary)

        print(f"Actual matrix {matrix}, returned {matrix_res}")

        for j in range(2):
            for k in range(2):
                if abs(matrix[j][k] - matrix_res[j][k]) > 0.1:
                    raise Exception(f"Incorrect coefficient at [{j}][{k}]: expected {matrix[j][k]}, got {matrix_res[j][k]}")