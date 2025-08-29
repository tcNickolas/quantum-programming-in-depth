from .boolean_operations import *
from psiqworkbench import QPU, Qubits
import pytest

# Classical functions
def f_not(args):
    return not args[0]

def f_xor(args):
   return args[0] != args[1]

def f_and(args):
   return args[0] and args[1]

def f_or(args):
   return args[0] or args[1]

def f_equal(args):
    return args[0] == args[1]

def f_multiand(args):
    return all(args)

def f_multior(args):
    return any(args)


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


@pytest.mark.parametrize("n, quantum_op, f", 
    [
      (1, quantum_not, f_not),
      (2, quantum_xor, f_xor),
      (2, quantum_and, f_and),
      (2, quantum_or, f_or),
      (2, quantum_equal, f_equal),
      (3, quantum_and, f_multiand),
      (3, quantum_or, f_multior)
    ])
def test_boolean_functions(n, quantum_op, f):
    run_test_reversible(n_inputs=n, n_qubits=n + 1, quantum_op=quantum_op, f=f)
