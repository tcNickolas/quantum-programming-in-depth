from .distinguish_bell_states import distinguish_bell_states
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from random import randrange

def prep_bell_state(ind):
  circ = QuantumCircuit(2)
  circ.h(0)
  circ.cx(0, 1)
  if ind // 2 == 1:
    circ.x(0)
  if ind % 2 == 1:
    circ.z(0)
  return circ

def test_distinguish_bell_states():
  for state_ind in range(4):
    circ = QuantumCircuit(2, 2)
    circ.append(prep_bell_state(state_ind), range(2))
    circ.append(distinguish_bell_states(), range(2), range(2))
    circ = circ.decompose()

    simulator = Aer.get_backend('aer_simulator')
    res_map = simulator.run(circ, shots=100).result().get_counts()
    # Check that the execution result is always the same
    assert len(res_map) == 1
    # Check that the measured state matches the state that was prepared
    res_state = int(list(res_map.keys())[0], 2)
    assert state_ind == res_state
