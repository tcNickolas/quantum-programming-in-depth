from .distinguish_unitaries import distinguish_x_z, distinguish_x_h, distinguish_x_minusx
import pytest
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

# Helper circuits that apply one of the two gates that 
# need to be distinguished, depending on the value of index
def apply_x_z(ind):
  circ = QuantumCircuit(1)
  if ind == 0:
    circ.x(0)
  else:
    circ.z(0)
  return circ

def apply_x_h(ind):
  circ = QuantumCircuit(1)
  if ind == 0:
    circ.x(0)
  else:
    circ.h(0)
  return circ

def apply_x_minusx(ind):
  circ = QuantumCircuit(1)
  if ind == 0:
    circ.x(0)
  else:
    circ.z(0)
    circ.x(0)
    circ.z(0)
  return circ

simulator = Aer.get_backend('aer_simulator')

@pytest.mark.parametrize("apply_unitaries,distinguisher",
                         [(apply_x_z, distinguish_x_z), 
                          (apply_x_h, distinguish_x_h), 
                          (apply_x_minusx, distinguish_x_minusx)])
def test_distinguish_unitaries(apply_unitaries, distinguisher):
  for unitary_ind in range(2):
    unitary_circ = apply_unitaries(unitary_ind)
    circ = distinguisher(unitary_circ)

    circ = transpile(circ, backend=simulator)
    res_map = simulator.run(circ, shots=100).result().get_counts()
    # Check that the execution result is always the same
    assert len(res_map) == 1
    # Check that the measured state matches the unitary that was passed
    res_unitary = int(list(res_map.keys())[0], 2)
    assert unitary_ind == res_unitary
