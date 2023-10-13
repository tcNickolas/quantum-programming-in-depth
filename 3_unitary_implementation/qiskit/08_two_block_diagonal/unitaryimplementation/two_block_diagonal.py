from math import atan2
from qiskit import QuantumCircuit

def apply_one_qubit(c):
  circ = QuantumCircuit(1)
  if abs(c[1][0]) > 1E-10 and abs(c[1][0] - c[0][1]) < 1E-10 or \
     abs(c[0][0]) > 1E-10 and abs(c[0][0] - c[1][1]) > 1E-10:
    circ.z(0)
  theta = atan2(c[1][0], c[0][0])
  circ.ry(2 * theta, 0)
  return circ.to_gate()

def apply_two_qubit_block_diagonal(a, b):
  circ = QuantumCircuit(2)
  circ.append(apply_one_qubit(b).control(1), [1, 0])
  circ.append(apply_one_qubit(a).control(1, ctrl_state=0), [1, 0])  
  return circ

def apply_two_qubit_cs_matrix(c0, s0, c1, s1):
  circ = QuantumCircuit(2)
  m0 = [[c0, -s0], [s0, c0]]
  m1 = [[c1, -s1], [s1, c1]]
  circ.append(apply_one_qubit(m1).control(1), [0, 1])
  circ.append(apply_one_qubit(m0).control(1, ctrl_state=0), [0, 1])  
  return circ

def apply_two_qubit_block_antidiagonal(a, b):
  circ = QuantumCircuit(2)
  id = [[1., 0.], [0., 1.]]
  minus_a = [[-a[0][0], -a[0][1]], [-a[1][0], -a[1][1]]]
  circ.append(apply_two_qubit_block_diagonal(id, minus_a), [0, 1])
  circ.append(apply_two_qubit_cs_matrix(*(0., 1.), *(0., 1.)), [0, 1])
  circ.append(apply_two_qubit_block_diagonal(id, b), [0, 1])
  return circ

def apply_arbitrary_unitary(n, u):
  # We cannot implement this completely yet, 
  # but we can implement some special cases.
  if n == 1:
    return apply_one_qubit(u)
  if n == 2:
    if all(v == 0 for v in 
           u[0][2:4] + u[1][2:4] + u[2][0:2] + u[3][0:2]):
      # Block-diagonal matrix.
      a = [u[0][0:2], u[1][0:2]]
      b = [u[2][2:4], u[3][2:4]]
      return apply_two_qubit_block_diagonal(a, b).decompose().to_gate()
    if all(v == 0 for v in 
           u[0][0:2] + u[1][0:2] + u[2][2:4] + u[3][2:4]):
      # Block-anti-diagonal matrix.
      a = [u[0][2:4], u[1][2:4]]
      b = [u[2][0:2], u[3][0:2]]
      return apply_two_qubit_block_antidiagonal(a, b).decompose().to_gate()
    raise NotImplementedError("The case of " +
      "arbitrary 2-qubit unitaries is not implemented yet")
  raise NotImplementedError(
    "The case of 3+-qubit unitaries is not implemented yet")

def apply_two_block_diagonal(n, a, b):
  circ = QuantumCircuit(n)
  circ.append(apply_arbitrary_unitary(n - 1, b).control(1), [n - 1] + list(range(n - 1)))
  circ.append(apply_arbitrary_unitary(n - 1, a).control(1, ctrl_state=0), [n - 1] + list(range(n - 1)))
  return circ
