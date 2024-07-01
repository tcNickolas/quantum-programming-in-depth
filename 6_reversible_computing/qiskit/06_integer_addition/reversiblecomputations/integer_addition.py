from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library.standard_gates import XGate

# Sum of n = 2 or 3 bits; last qubit is sum
def sum_mod_two(n):
  circ = QuantumCircuit(n + 1)
  for i in range(n):
    circ.cx(i, n)
  return circ

# Carry of n = 2 or 3 bits; last qubit is carry
def carry(n):
  circ = QuantumCircuit(n + 1)
  for i in range(n - 1):
    for j in range(i + 1, n):
      circ.ccx(i, j, n)
  return circ

# Use big endian to store numbers
def adder(n):
  if n == 1:
    # No need for carry
    return sum_mod_two(2)
  
  x = QuantumRegister(n)
  y = QuantumRegister(n)
  sum = QuantumRegister(n)
  carry_bits = QuantumRegister(n - 1)
  circ = QuantumCircuit(x, y, carry_bits, sum)

  # Compute carry bits first
  circ.append(carry(2), [x[n - 1], y[n - 1], carry_bits[n - 2]])
  for i in range(n - 2, 0, -1):
    circ.append(carry(3), [x[i], y[i], carry_bits[i], carry_bits[i - 1]])
  
  # Compute sum bits
  circ.append(sum_mod_two(2), [x[n - 1], y[n - 1], sum[n - 1]])
  for i in range(n - 2, -1, -1):
    circ.append(sum_mod_two(3), [x[i], y[i], carry_bits[i], sum[i]])
  
  # Uncompute carry bits (adjoint of compute)
  for i in range(1, n - 1):
    circ.append(carry(3), [x[i], y[i], carry_bits[i], carry_bits[i - 1]])
  circ.append(carry(2), [x[n - 1], y[n - 1], carry_bits[n - 2]])

  return circ
