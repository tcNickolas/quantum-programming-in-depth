from qiskit import QuantumCircuit

def read_info(n):
  circ = QuantumCircuit(n, n)
  circ.measure(range(n), range(n))
  return circ
