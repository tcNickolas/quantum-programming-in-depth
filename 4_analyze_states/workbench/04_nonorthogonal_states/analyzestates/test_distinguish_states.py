from math import pi, cos, sin
from random import uniform
from psiqworkbench import QPU, Qubits
from .distinguish_states import distinguish_zero_and_sup

def prep_test_state(reg: Qubits, alpha: float, beta: float, ind: int) -> None:
    amps = [[1, 0],
            [alpha, beta]
            ]
    reg.push_state(amps[ind])


def test_distinguish_states():
    qpu = QPU()
    for _ in range(10):
        angle = uniform(0, pi / 2)
        (alpha, beta) = (cos(angle), sin(angle))

        n_correct = 0
        n_trials_each = 1000
        for state_ind in range(2):
            for _ in range(n_trials_each):
                qpu.reset(1)
                reg = Qubits(1, "reg", qpu)
                prep_test_state(reg, alpha, beta, state_ind)
                ind = distinguish_zero_and_sup(reg, alpha, beta)
                n_correct += (ind == state_ind)
        p_success = n_correct / (2 * n_trials_each)
        p_success_theor = 0.5 * (1 + beta)                
        assert abs(p_success - p_success_theor) < 0.05