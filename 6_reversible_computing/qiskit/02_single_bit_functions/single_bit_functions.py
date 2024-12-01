from math import acos
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library.standard_gates import XGate
from qiskit_aer import Aer

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

simulator = Aer.get_backend('aer_simulator')

for (quantum_op, f) in [
    (quantum_zero, "f(x) = 0"), 
    (quantum_one, "f(x) = 1"), 
    (quantum_x, "f(x) = x"),
    (quantum_one_minus_x, "f(x) = 1 - x") ]:
  circ = QuantumCircuit(2)
  circ.ry(2 * acos(0.6), 0)
  circ.append(quantum_op(), [0, 1])
  circ.save_statevector()

  circ = transpile(circ, backend=simulator)
  state_vector = simulator.run(circ).result().get_statevector()
  print(f"The effects of applying the quantum operation {f} to the state (0.6|0⟩ + 0.8|1⟩) ⨂ |0⟩:")
  # Qiskit uses little endian: qubit 0 is printed last in ket notation
  print(state_vector.draw(output='latex_source'))
