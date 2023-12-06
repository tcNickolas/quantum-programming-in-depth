from qiskit import QuantumCircuit

def distinguish_bell_states():
  circ = QuantumCircuit(2, 2)
  circ.cnot(0, 1)
  circ.h(0)
  circ.measure(range(2), range(2))
  return circ
