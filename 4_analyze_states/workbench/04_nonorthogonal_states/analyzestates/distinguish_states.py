from math import atan2, pi
from psiqworkbench import Qubits, Units

def distinguish_zero_and_sup(reg: Qubits, alpha: float, beta: float) -> int:
    theta = atan2(beta, alpha) / 2
    reg.ry(- 2 * (theta - pi / 4) * Units.rad)
    return reg.read()
