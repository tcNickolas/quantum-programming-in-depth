from .read_info import read_info
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from random import randint

def run_test_read_info(n, num):
  circ = QuantumCircuit(n, n)
  for i in range(n):
    if (num & (1 << i)) > 0:
      circ.x(i)

  circ.append(read_info(n), range(n), range(n))
  circ = circ.decompose()

  simulator = Aer.get_backend('aer_simulator')
  res_map = simulator.run(circ, shots=1).result().get_counts()
  res_bitstring = list(res_map.keys())[0]
  res = int(res_bitstring, 2)

  assert res == num

def test_read_info():
  for _ in range(1, 20):
    n = randint(1, 5)
    num = randint(0, 2 ** n - 1)
    run_test_read_info(n, num)
