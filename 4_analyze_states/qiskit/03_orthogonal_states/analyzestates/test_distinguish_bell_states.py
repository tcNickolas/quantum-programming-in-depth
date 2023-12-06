from .distinguish_bell_states import distinguish_bell_states
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from random import randrange

def prep_bell_state(ind):
  circ = QuantumCircuit(2)
  circ.h(0)
  circ.cnot(0, 1)
  if ind // 2 == 1:
    circ.x(0)
  if ind % 2 == 1:
    circ.z(0)
  return circ

def test_distinguish_bell_states():
  for _ in range(100):
    state_ind = randrange(0, 4)

    circ = QuantumCircuit(2, 2)
    circ.append(prep_bell_state(state_ind), range(2))
    circ.append(distinguish_bell_states(), range(2), range(2))
    circ = circ.decompose()

    simulator = Aer.get_backend('aer_simulator')
    res_map = simulator.run(circ, shots=1).result().get_counts()
    res_state = int(list(res_map.keys())[0], 2)
    
    assert state_ind == res_state
