from math import atan2, sqrt
from psiqworkbench import QPU, Qubits, Units

def prep_two_qubit(reg: Qubits, amps: list[float]) -> None:
    b0 = sqrt(amps[0]**2 + amps[2]**2)
    b1 = sqrt(amps[1]**2 + amps[3]**2)

    theta = 2 * atan2(b1, b0)
    reg[0].ry(theta * Units.rad)

    theta0 = 2 * atan2(amps[2], amps[0])
    reg[1].ry(theta0 * Units.rad, cond=~reg[0])

    theta1 = 2 * atan2(amps[3], amps[1])
    reg[1].ry(theta1 * Units.rad, cond=reg[0])
