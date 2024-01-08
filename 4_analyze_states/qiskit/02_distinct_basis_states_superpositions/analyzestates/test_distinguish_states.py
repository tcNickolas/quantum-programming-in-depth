from .read_info import read_info
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from random import randint

def prep_test_state(ind):
  circ = QuantumCircuit(3)
  circ.h(0)
  circ.cnot(0, 1)
  circ.cnot(0, 2)
  if ind > 0:
    circ.x(ind - 1)
  return circ

def interpret_measurements(str):
  res = int(str, 2)
  return res if res < 4 else 7 - res

def test_distinguish_states():
  for state_ind in range(4):
    circ = QuantumCircuit(3, 3)
    circ.append(prep_test_state(state_ind), range(3))
    circ.append(read_info(3), range(3), range(3))
    circ = circ.decompose()

    simulator = Aer.get_backend('aer_simulator')
    res_map = simulator.run(circ, shots=100).result().get_counts()
    # Check that for each execution result the state is intepreted correctly
    for key in list(res_map.keys()):
      assert interpret_measurements(key) == state_ind
