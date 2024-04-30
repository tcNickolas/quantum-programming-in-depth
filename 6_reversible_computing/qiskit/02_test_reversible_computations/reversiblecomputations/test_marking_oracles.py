from cmath import isclose
from .marking_oracles import oracle_zero, oracle_one, oracle_x
import pytest
from qiskit import QuantumCircuit
from qiskit_aer import Aer

def f_zero(arg):
  return False

def f_one(arg):
  return True

def f_x(arg):
  return arg

simulator = Aer.get_backend('aer_simulator')

@pytest.mark.parametrize("oracle,f",
                         [(oracle_zero, f_zero),
                          (oracle_one, f_one),
                          (oracle_x, f_x)])
def test_marking_oracle(oracle, f):
  for input in [False, True]:
    circ = QuantumCircuit(2)
    if input:
      circ.x(0)
    circ.append(oracle(), [0, 1])

    expected = f(input)
    if expected:
      circ.x(1)

    if input:
      circ.x(0)

    circ = circ.decompose()
    circ.save_statevector()

    res = simulator.run(circ).result()
    state_vector = res.get_statevector().data

    non_zeros = [not isclose(amp, 0, abs_tol=1e-9) for amp in state_vector]
    if any(non_zeros[1:]):
      # Either result is incorrect or inputs are modified.
      # Result is stored in most significant bit, input - in least significant bit
      count = non_zeros.count(True)
      if count > 1:
        raise Exception(f"Unexpected result for input {input}: the state should not be a superposition")

      index = non_zeros.index(True)
      if index // 2 > 0:
        raise Exception(f"Unexpected result for input {input}: expected {expected}, got {not expected}")
      else:
        raise Exception(f"Unexpected result for input {input}: the state of the input qubit was modified")
