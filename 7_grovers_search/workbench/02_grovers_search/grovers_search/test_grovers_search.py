from functools import partial
from psiqworkbench import QPU, Qubits
from .grovers_search import *
import pytest


test_cases = [
      (2, [0]),
      (2, [1]),
      (3, [0, 3]),
      (3, [1, 4]),
      (3, [2, 7])
    ]

@pytest.mark.parametrize("n, marked_states", test_cases)
def test_grovers_search(n, marked_states):
    oracle = partial(marking_oracle, marked_states=marked_states)
    # Run Grover's search end-to-end and check that 
    # the result is the big endian representation of one of the marked states 100% of the time
    n_runs = 100
    n_correct = 0
    for _ in range(n_runs):
        res = run_grovers_search(n, oracle, 1)
        if res in marked_states:
            n_correct += 1
    assert n_correct == n_runs