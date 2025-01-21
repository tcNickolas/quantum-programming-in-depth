from random import randint
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from .read_info import read_info

simulator = AerSimulator(method='statevector')

def run_test_read_info(n, basis_state):
  circ = QuantumCircuit(n, n)
  for i in range(n):
    if basis_state & (1 << i) > 0:
      circ.x(i)

  circ.append(read_info(n), range(n), range(n))

  circ = transpile(circ, backend=simulator)
  res_map = simulator.run(circ, shots=100).result().get_counts()
  # Check that the execution result is always the same
  assert len(res_map) == 1
  # Check that the measured state matches the state that was prepared
  res_bitstring = list(res_map.keys())[0]
  res = int(res_bitstring, 2)

  assert res == basis_state

def test_read_info():
  for _ in range(1, 20):
    n = randint(1, 5)
    num = randint(0, 2 ** n - 1)
    run_test_read_info(n, num)
