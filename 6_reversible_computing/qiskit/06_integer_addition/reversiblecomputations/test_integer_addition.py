from cmath import isclose
from .integer_addition import adder
import pytest
from qiskit import QuantumCircuit, QuantumRegister
from qiskit_aer import Aer

simulator = Aer.get_backend('aer_simulator')

def int_as_be(n, a):
  format_str = f"{{:0>{n}b}}"
  a_str = format_str.format(a)
  return [a_str[i] == '1' for i in range(n)]

def run_test_adder(n):

  for a_int in range(2 ** n):
    for b_int in range(2 ** n):
      sum_int = (a_int + b_int) % (2 ** n)
      a_be = int_as_be(n, a_int)
      b_be = int_as_be(n, b_int)
      sum_be = int_as_be(n, sum_int)

      x = QuantumRegister(n)
      y = QuantumRegister(n)
      sum = QuantumRegister(n)
      carry_bits = QuantumRegister(n - 1)
      circ = QuantumCircuit(x, y, carry_bits, sum)

      # Compute inputs.
      for i in range(n):
        if a_be[i]:
          circ.x(x[i])

      for i in range(n):
        if b_be[i]:
          circ.x(y[i])

      circ.append(adder(n), range(4 * n - 1))

      # Uncompute inputs.
      for i in range(n):
        if a_be[i]:
          circ.x(x[i])

      for i in range(n):
        if b_be[i]:
          circ.x(y[i])

      for i in range(n):
        if sum_be[i]:
          circ.x(sum[i])

      circ = circ.decompose(reps=4)
      circ.save_statevector()

      res = simulator.run(circ).result()
      state_vector = res.get_statevector().data

      print(state_vector)

      non_zeros = [not isclose(amp, 0, abs_tol=1e-9) for amp in state_vector]
      if any(non_zeros[1:]):
        # Either result is incorrect or inputs are modified.
        count = non_zeros.count(True)
        if count > 1:
          raise Exception(f"Unexpected result for inputs x={a_int}, y={b_int}: the state should not be a superposition")

        index = non_zeros.index(True)
        index_be = int_as_be(4 * n - 1, index)
        # The first n bits are sum, the next n-1 - carry, after that - y and x
        if any(index[0:n]):
          raise Exception(f"Unexpected result for inputs x={a_int}, y={b_int}: incorrect sum")
        if any(index[n:2 * n - 1]):
          raise Exception(f"Unexpected result for inputs x={a_int}, y={b_int}: carry register not uncomputed")
        raise Exception(f"Unexpected result for inputs x={a_int}, y={b_int}: the state of input qubits was modified")


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_adder(n):
  run_test_adder(n)
