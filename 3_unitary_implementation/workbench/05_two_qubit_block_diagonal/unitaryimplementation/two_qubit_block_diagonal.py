from math import atan2, isclose
from psiqworkbench import Qubits, Qubrick, Units

class ApplyOneQubitUnitary(Qubrick):
    def _compute(self, reg: Qubits, u: list[list[float]], ctrl: Qubits=0) -> None:
        if isclose(u[0][0], -u[1][1]) and isclose(u[1][0], u[0][1]):
            reg.z(cond=ctrl)
        theta = atan2(u[1][0], u[0][0])
        reg.ry(2 * theta * Units.rad, cond=ctrl)


class ApplyTwoQubitBlockDiagonal(Qubrick):
    def __init__(self, name=None, **kwargs):
        super().__init__(name, never_uncompute=True, **kwargs)
        self.one_qubit = ApplyOneQubitUnitary()
    def _compute(self, reg: Qubits, a: list[list[float]], b: list[list[float]]) -> None:
        self.one_qubit.compute(reg[0], b, ctrl=reg[1])
        self.one_qubit.compute(reg[0], a, ctrl=~reg[1])
