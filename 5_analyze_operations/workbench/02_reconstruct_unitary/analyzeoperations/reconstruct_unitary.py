from math import atan2, pi, sqrt
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
    

def reconstruct_unitary(gate: callable) -> list[list[float]]:
    # Analyze the effects of the gate on the |0> state to get the first column
    (a, b) = reconstruct_state(gate)

    # Figure out whether the second column is (b; -a) or (-b; a)
    # Prepare a state a|0> + b|1> and apply the unitary to it; 
    # in the first case, the result is always |0>, in the second case, (a^2-b^2)|0> + 2ab|1>
    n_trials = 1000
    n0 = 0
    qpu = QPU()
    for _ in range(n_trials):
        qpu.reset(1)
        reg = Qubits(1, "reg", qpu)

        # Prepare a state a|0> + b|1> using the unitary itself and apply the unitary to it again
        gate(reg)
        gate(reg)
        if b < 0:
            reg.z()
        # Treat the result as a choice between |0> and (a^2-b^2)|0> + 2ab|1>
        # Figure out the angle of the line halfway between |0> and alpha |0> + beta |1>
        theta = atan2(2 * a * abs(b), a * a - b * b) / 2
        # Rotate so that the middle between the two angles is at the angle pi/4
        reg.ry(- 2 * (theta - pi / 4) * Units.rad)
        if reg.read() == 0:
            n0 += 1

    if 2 * n0 > n_trials:
        return [[a, b], [b, -a]]
    else:
        return [[a, -b], [b, a]]