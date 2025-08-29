from math import atan2, isclose
from psiqworkbench import Qubits, Qubrick, Units

class ApplyOneQubitUnitary(Qubrick):
    def _compute(self, reg: Qubits, u: list[list[float]], ctrl: Qubits=0) -> None:
        if isclose(u[0][0], -u[1][1]) and isclose(u[1][0], u[0][1]):
            reg.z(cond=ctrl)
        theta = atan2(u[1][0], u[0][0])
        reg.ry(2 * theta * Units.rad, cond=ctrl)


class ApplyTwoQubitCSMatrix(Qubrick):
    def __init__(self, name=None, **kwargs):
        super().__init__(name, never_uncompute=True, **kwargs)
        self.one_qubit = ApplyOneQubitUnitary()
    def _compute(self, reg: Qubits, c0: float, s0: float, c1: float, s1: float) -> None:
        m0 = [[c0, -s0], [s0, c0]]
        m1 = [[c1, -s1], [s1, c1]]
        self.one_qubit.compute(reg[1], m1, ctrl=reg[0])
        self.one_qubit.compute(reg[1], m0, ctrl=~reg[0])
