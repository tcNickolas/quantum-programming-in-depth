from cmath import isclose
from qiskit import QuantumCircuit
from qiskit_aer import Aer
import pytest
from .boolean_operations import *

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


simulator = Aer.get_backend('aer_simulator')

@pytest.mark.parametrize("n, quantum_op, f", 
    [
      (1, quantum_not(), f_not),
      (2, quantum_xor(), f_xor),
      (2, quantum_and(), f_and),
      (2, quantum_or(), f_or),
      (2, quantum_equal(), f_equal),
      (2, quantum_multiand(2), f_multiand),
      (3, quantum_multiand(3), f_multiand),
      (2, quantum_multior(2), f_multior),
      (3, quantum_multior(3), f_multior)
    ])
def test_logic_operation(n, quantum_op, f):
  format_str = f"{{:0>{n}b}}"
  for input in range(2 ** n):
    input_str = format_str.format(input)
    input_be = [input_str[i] == '1' for i in range(n)]

    circ = QuantumCircuit(n + 1)
    for i in range(n):
      if input_be[i]:
        circ.x(i)

    circ.append(quantum_op, range(n + 1))

    expected = f(input_be)
    if expected:
      circ.x(n)

    for i in range(n):
      if input_be[i]:
        circ.x(i)

    circ = circ.decompose(reps=2)
    circ.save_statevector()

    res = simulator.run(circ).result()
    state_vector = res.get_statevector().data

    non_zeros = [not isclose(amp, 0, abs_tol=1e-9) for amp in state_vector]
    if any(non_zeros[1:]):
      # Either result is incorrect or inputs are modified.
      # Result is stored in most significant bit, input - in least significant bit
      prefix = f"Error for x={input}:"
      count = non_zeros.count(True)
      if count > 1:
        raise Exception(f"{prefix} the state should not be a superposition")

      index = non_zeros.index(True)
      if index // (2 ** (n - 1)) > 0:
        raise Exception(f"{prefix} expected {expected}, got {not expected}")
      else:
        raise Exception(f"{prefix} the state of the input qubits changed")
