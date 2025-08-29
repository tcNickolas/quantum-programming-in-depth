from math import atan2, isclose
from psiqworkbench import Qubits, Qubrick, Units

class ApplyOneQubitUnitary(Qubrick):
    def _compute(self, reg: Qubits, u: list[list[float]]) -> None:
        assert reg.num_qubits == 1
        if isclose(u[0][0], -u[1][1]) and isclose(u[1][0], u[0][1]):
            reg.z()
        theta = atan2(u[1][0], u[0][0])
        reg.ry(2 * theta * Units.rad)
