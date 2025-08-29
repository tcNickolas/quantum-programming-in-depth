from .single_bit_functions import *
from psiqworkbench import QPU, Qubits
import pytest

# Classical functions
def f_zero(arg):
    return False

def f_one(arg):
    return True

def f_x(arg):
    return arg

def f_one_minus_x(arg):
    return not arg

@pytest.mark.parametrize("quantum_op,f",
                         [(quantum_zero, f_zero),
                          (quantum_one, f_one),
                          (quantum_x, f_x),
                          (quantum_one_minus_x, f_one_minus_x)])
def test_single_bit_functions(quantum_op, f):
    qpu = QPU(filters=['>>bit-qpu>>'])
    for input in [False, True]:
        qpu.reset(2)
        x = Qubits(1, "x", qpu)
        y = Qubits(1, "y", qpu)
        if input:
            x.x()

        quantum_op(x, y)

        res_expected = f(input)

        res_x = x.read()
        res_y = y.read()

        if res_x != input:
            raise Exception(f"Error for x={input}: the state of the input qubit changed")
        if res_y != res_expected:
            raise Exception(f"Error for x={input}: expected {res_expected}, got {res_y}")                