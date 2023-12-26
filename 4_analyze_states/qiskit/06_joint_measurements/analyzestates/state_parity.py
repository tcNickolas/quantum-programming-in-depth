from qiskit import QuantumCircuit

def state_parity(n):
  circ = QuantumCircuit(n + 1, 1)
  for i in range(n):
    circ.cnot(i, n)
  circ.measure(n, 0)
  return circ
