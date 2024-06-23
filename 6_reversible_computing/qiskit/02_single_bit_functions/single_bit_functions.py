from math import acos
from qiskit import QuantumCircuit
from qiskit.circuit.library.standard_gates import XGate
from qiskit_aer import Aer

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

def oracle_one_minus_x():
  circ = QuantumCircuit(2)
  circ.append(XGate().control(1, ctrl_state=0), [0, 1])
  return circ

simulator = Aer.get_backend('aer_simulator')

for (oracle, f) in [
   (oracle_zero, "f(x) = 0"), 
   (oracle_one, "f(x) = 1"), 
   (oracle_x, "f(x) = x"),
   (oracle_one_minus_x, "f(x) = 1 - x"),
  ]:
  circ = QuantumCircuit(2)
  circ.ry(2 * acos(0.6), 0)
  circ.append(oracle(), [0, 1])
  circ = circ.decompose(reps=3)
  circ.save_statevector()

  res = simulator.run(circ).result()
  state_vector = res.get_statevector()
  print(f"The effects of applying the oracle {f} to the state (0.6|0⟩ + 0.8|1⟩) ⨂ |0⟩:")
  # Qiskit uses little endian: qubit 0 is printed last in ket notation
  print(state_vector.draw(output='latex_source'))
