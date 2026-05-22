from math import atan2, pi
from psiqdk.workbench import Qubits, units

def distinguish_zero_and_sup(reg: Qubits, alpha: float, beta: float) -> int:
    theta = atan2(beta, alpha) / 2
    reg.ry(- 2 * (theta - pi / 4) * units.rad)
    return reg.read()
