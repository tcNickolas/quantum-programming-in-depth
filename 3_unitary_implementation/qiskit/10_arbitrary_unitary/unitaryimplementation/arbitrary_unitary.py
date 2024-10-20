from math import atan2, isclose
from qiskit import QuantumCircuit
from scipy.linalg import cossin

def apply_one_qubit(u):
  circ = QuantumCircuit(1)
  if isclose(u[0][0], -u[1][1]) and isclose(u[1][0], u[0][1]):
    circ.z(0)
  theta = atan2(u[1][0], u[0][0])
  circ.ry(2 * theta, 0)
  return circ.to_gate()

def apply_arbitrary_cs_matrix(n, cs):
  circ = QuantumCircuit(n)
  for (k, (c, s)) in enumerate(cs):
    m = [[c, -s], [s, c]]
    circ.append(apply_one_qubit(m).control(n - 1, ctrl_state=k), range(n))
  return circ

def apply_two_block_diagonal(n, a, b):
  circ = QuantumCircuit(n)
  circ.append(apply_arbitrary_unitary(n - 1, b).control(1), 
              [n - 1] + list(range(n - 1)))
  circ.append(apply_arbitrary_unitary(n - 1, a).control(1, ctrl_state=0), 
              [n - 1] + list(range(n - 1)))
  return circ

def apply_arbitrary_unitary(n, u):
  if n == 1:
    return apply_one_qubit(u)
    
  circ = QuantumCircuit(n)

  # Get the cosine-sine decomposition.
  left, cs, right = cossin(u, p=len(u) / 2, q=len(u) / 2) 

  # Apply right - a two-block-diagonal unitary.
  ar, br = extract_blocks(right)
  circ.append(apply_two_block_diagonal(n, ar, br), range(n))

  # Apply cs - an arbitrary cs matrix.
  cs_pairs = []
  for i in range(len(cs) // 2):
    cs_pairs += [(cs[i][i], cs[i + len(cs) // 2][i])]
  circ.append(apply_arbitrary_cs_matrix(n, cs_pairs), range(n))

  # Apply left - a two-block-diagonal unitary.
  al, bl = extract_blocks(left)
  circ.append(apply_two_block_diagonal(n, al, bl), range(n))
  return circ.decompose().to_gate()

def extract_blocks(matrix):
  # Double-check that the blocks outside the main diagonal are zeros.
  block_len = len(matrix) // 2

  if any(any(element != 0 for element in row[block_len : ]) for row in matrix[0 : block_len]) or \
     any(any(element != 0 for element in row[0 : block_len]) for row in matrix[block_len : ]):
    raise ValueError("Matrix should be block-diagonal")

  a = [row[0 : block_len] for row in matrix[0 : block_len]]
  b = [row[block_len : ] for row in matrix[block_len : ]]
  return (a, b)
