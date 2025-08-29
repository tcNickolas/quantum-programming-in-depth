from functools import partial
from math import pi, cos, sin
from random import randrange, uniform
from psiqworkbench import Qubits
from .reconstruct_state import reconstruct_state

def prep_test_state(reg: Qubits, amps: list[float]) -> None:
    reg.push_state(amps)


def test_reconstruct_states():
    for _ in range(50):
        angle = uniform(0.1, pi / 2 - 0.1)
        alpha = cos(angle)
        beta = (1 if randrange(2) == 0 else -1) * sin(angle)

        state_prep = partial(prep_test_state, amps=[alpha, beta])

        (alpha_res, beta_res) = reconstruct_state(state_prep)

        print(f"Actual amplitudes {alpha},{beta}, returned {alpha_res},{beta_res}")
        assert abs(alpha - alpha_res) < 0.1 and abs(beta - beta_res) < 0.1