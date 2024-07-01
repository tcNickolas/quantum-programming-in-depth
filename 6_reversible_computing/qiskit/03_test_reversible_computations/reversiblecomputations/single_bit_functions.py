from qiskit import QuantumCircuit
from qiskit.circuit.library.standard_gates import XGate

def quantum_zero():
  circ = QuantumCircuit(2)
  # Do nothing.
  return circ

def quantum_one():
  circ = QuantumCircuit(2)
  circ.x(1)
  return circ

def quantum_x():
  circ = QuantumCircuit(2)
  circ.cx(0, 1)
  return circ

def quantum_one_minus_x():
  circ = QuantumCircuit(2)
  circ.append(XGate().control(1, ctrl_state=0), [0, 1])
  return circ
