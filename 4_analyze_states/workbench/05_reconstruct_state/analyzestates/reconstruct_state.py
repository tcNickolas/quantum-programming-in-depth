from math import pi, sqrt
from psiqworkbench import QPU, Qubits, Units

def reconstruct_state(state_prep: callable) -> tuple[float, float]:
    n_trials = 1000

    # Figure out the absolute values of alpha and beta
    qpu = QPU()

    n0 = 0
    for _ in range(n_trials):
        qpu.reset(1)
        reg = Qubits(1, "reg", qpu)
        state_prep(reg)
        if reg.read() == 0:
            n0 += 1
    n1 = n_trials - n0
    alpha = sqrt(n0 / n_trials)
    beta = sqrt(n1 / n_trials)    

    # Figure out whether there is a relative phase of -1
    # (distinguish alpha |0> + beta |1> from alpha |0> - beta |1>).
    n0 = 0
    for _ in range(n_trials):
        qpu.reset(1)
        reg = Qubits(1, "reg", qpu)
        state_prep(reg)
        # The mid-line between them would be horizontal, so we rotate by PI/4 clockwise
        reg.ry(pi / 2 * Units.rad)
        if reg.read() == 0:
            n0 += 1
    if 2 * n0 > n_trials:
        return (alpha, -beta)
    else:
        return (alpha, beta)