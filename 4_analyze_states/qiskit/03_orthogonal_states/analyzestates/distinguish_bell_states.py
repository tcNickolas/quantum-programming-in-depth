from qiskit import QuantumCircuit

def distinguish_bell_states():
  circ = QuantumCircuit(2, 2)
  circ.cx(0, 1)
  circ.h(0)
  circ.measure(range(2), range(2))
  return circ
