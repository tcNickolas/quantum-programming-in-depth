from math import atan2, sqrt
from psiqworkbench import Qubits, Qubrick, Units

class StatePrep(Qubrick):
    def _compute(self, input_reg: Qubits, amps: list[float], ctrl=0):
        if input_reg.num_qubits == 1:
            theta = 2 * atan2(amps[1], amps[0])
            input_reg.ry(theta * Units.rad, cond=ctrl)
        else:
            even_amps = amps[0::2]
            odd_amps = amps[1::2]
            b0 = sqrt(sum(a * a for a in even_amps))
            b1 = sqrt(sum(a * a for a in odd_amps))

            self.compute(input_reg[0], [b0, b1], ctrl=ctrl)

            # Controlled-on-zero state prep on n-1 most significant qubits
            # input[0].x()
            self.compute(input_reg[1:], even_amps, ctrl=ctrl | ~input_reg[0])
            # input[0].x()

            # Controlled state prep on n-1 most significant qubits
            self.compute(input_reg[1:], odd_amps,  ctrl=ctrl | input_reg[0])
