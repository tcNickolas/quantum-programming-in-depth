from qiskit import QuantumCircuit

def oracle_zero():
  circ = QuantumCircuit(2)
  # Do nothing.
  return circ

def oracle_one():
  circ = QuantumCircuit(2)
  circ.x(1)
  return circ

def oracle_x():
  circ = QuantumCircuit(2)
  circ.cx(0, 1)
  return circ
