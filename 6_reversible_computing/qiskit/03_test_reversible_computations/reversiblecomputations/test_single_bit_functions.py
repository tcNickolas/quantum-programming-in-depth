from cmath import isclose
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import pytest
from .single_bit_functions import *

def f_zero(arg):
  return False

def f_one(arg):
  return True

def f_x(arg):
  return arg

def f_one_minus_x(arg):
  return not arg

simulator = Aer.get_backend('aer_simulator')

@pytest.mark.parametrize("quantum_op,f",
                         [(quantum_zero, f_zero),
                          (quantum_one, f_one),
                          (quantum_x, f_x),
                          (quantum_one_minus_x, f_one_minus_x)])
def test_reversible_computation(quantum_op, f):
  for input in [False, True]:
    circ = QuantumCircuit(2)
    if input:
      circ.x(0)
    circ.append(quantum_op(), [0, 1])

    expected = f(input)
    if expected:
      circ.x(1)

    if input:
      circ.x(0)

    circ.save_statevector()
    circ = transpile(circ, backend=simulator)

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
      if index // 2 > 0:
        raise Exception(f"{prefix} expected {expected}, got {not expected}")
      else:
        raise Exception(f"{prefix} the state of the input qubit changed")
