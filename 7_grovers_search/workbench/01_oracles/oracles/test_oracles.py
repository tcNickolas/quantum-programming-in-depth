from functools import partial
from psiqworkbench import QPU, Qubits
from .oracles import *
import pytest

def run_test_reversible(n_inputs: int, n_qubits: int, quantum_op: callable, f: callable):
    qpu = QPU(filters=['>>bit-qpu>>'])
    for input in range(2 ** n_inputs):
        qpu.reset(n_qubits)
        x = Qubits(n_inputs, "x", qpu)
        y = Qubits(1, "y", qpu)
        if input > 0:
            x.x(input)

        quantum_op(x, y)
       
        input_str = (f"{{:0>{n_inputs}b}}").format(input)
        input_le = [input_str[i] == '1' for i in range(n_inputs)][::-1]
        res_expected = f(input_le)

        res_x = x.read()
        res_y = y.read()

        if res_x != input:
            raise Exception(f"Error for x={input}: the state of the input qubit changed")
        if res_y != res_expected:
            raise Exception(f"Error for x={input}: expected {res_expected}, got {res_y}")                


def f_mark_states(args: list[bool], marked_states: list[int]) -> bool:
    # Use big endian to convert Boolean array to integer
    arg = int("".join(["1" if a else "0" for a in args]), 2)
    return arg in marked_states


test_cases = [
      (1, []),
      (1, [1]),
      (2, [1]),
      (2, [2]),
      (2, [0, 3]),
      (3, [0, 3, 6]),
      (3, [1, 3, 5, 7])
    ]


@pytest.mark.parametrize("n, marked_states", test_cases)
def test_marking_oracle(n, marked_states):
    f = partial(f_mark_states, marked_states=marked_states)
    quantum_op = partial(marking_oracle, marked_states=marked_states)
    run_test_reversible(n, n + 1, quantum_op, f)


@pytest.mark.parametrize("n, marked_states", test_cases)
def test_phase_oracle(n, marked_states):
    qpu = QPU(num_qubits=n + 1, filters=">>unitary>>")
    reg = Qubits(n, "reg", qpu)

    phase_oracle(reg, partial(marking_oracle, marked_states=marked_states))

    ufilter = qpu.get_filter_by_name('>>unitary>>')
    matrix = ufilter.get()

    # Construct the matrix of the phase oracle (taking into account the auxiliary qubit)
    complete_coef = []
    for state in range(2 ** (n + 1)):
        row = [0] * 2 ** (n + 1)
        row[state] = 1
        complete_coef += [row]
    # Mark only the states where phase is flipped
    for state in marked_states:
        stateLE = int((f"{{:0>{n}b}}".format(state))[::-1], 2)
        complete_coef[stateLE][stateLE] = -1

    for actual, expected in zip(matrix, complete_coef):
        assert actual == pytest.approx(expected)
    