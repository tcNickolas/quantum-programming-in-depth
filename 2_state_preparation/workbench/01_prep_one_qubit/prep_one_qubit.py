from math import atan2
from psiqworkbench import QPU, Qubits, Units

alpha, beta = 0.6, 0.8
theta = 2 * atan2(beta, alpha)

qpu = QPU(num_qubits=1)
reg = Qubits(1, "reg", qpu)

theta = 2 * atan2(beta, alpha)
reg.ry(theta * Units.rad)
