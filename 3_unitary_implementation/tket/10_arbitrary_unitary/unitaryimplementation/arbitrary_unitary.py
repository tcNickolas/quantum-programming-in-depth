from pytest import approx
from math import atan2, isclose, pi, ceil, log2
from pytket.circuit import Circuit, CircBox, QControlBox
from scipy.linalg import cossin

def apply_one_qubit(u):
  circ = Circuit(1)
  if isclose(u[0][0], -u[1][1]) and isclose(u[1][0], u[0][1]):
    circ.Z(0)
  theta = atan2(u[1][0], u[0][0])
  circ.Ry(2 * (theta / pi), 0)
  circ_gate = CircBox(circ)
  return circ_gate
def apply_arbitrary_cs_matrix(n, cs):
  circ = Circuit(n)
  for (k, (c, s)) in enumerate(cs):
    m = [[c, -s], [s, c]]
    control = QControlBox(apply_one_qubit(m), n_controls=n-1, control_state=k)
    circ.add_qcontrolbox(control, list(range(1, n)) + [0])
  circ_gate = CircBox(circ)
  return circ_gate

def apply_two_block_diagonal(n, a, b):
  circ = Circuit(n)
  control_1 = QControlBox(apply_arbitrary_unitary(n-1, b), n_controls=1)
  control_0 = QControlBox(apply_arbitrary_unitary(n-1, a), n_controls=1, control_state=0)
  circ.add_qcontrolbox(control_1, list(range(n)))
  circ.add_qcontrolbox(control_0, list(range(n)))
  circ_gate = CircBox(circ)
  return circ_gate
  return circ


def apply_arbitrary_unitary(n, u):
  if n == 1:
    return apply_one_qubit(u)
    
  circ = Circuit(n)

  # Get the cosine-sine decomposition.
  left, cs, right = cossin(u, p=len(u) / 2, q=len(u) / 2) 

  # Apply right - a two-block-diagonal unitary.
  ar, br = extract_blocks(right)
  circ.add_circbox(apply_two_block_diagonal(n, ar, br), range(n))

  # Apply cs - an arbitrary cs matrix.
  cs_pairs = []
  for i in range(len(cs) // 2):
    cs_pairs += [(cs[i][i], cs[i + len(cs) // 2][i])]
  circ.add_circbox(apply_arbitrary_cs_matrix(n, cs_pairs), range(n))

  # Apply left - a two-block-diagonal unitary.
  al, bl = extract_blocks(left)
  circ.add_circbox(apply_two_block_diagonal(n, al, bl), range(n))
  circ_gate = CircBox(circ)
  return circ_gate

def extract_blocks(matrix):
  # Double-check that the blocks outside the main diagonal are zeros.
  block_len = len(matrix) // 2

  if any(any(element != 0 for element in row[block_len : ]) for row in matrix[0 : block_len]) or \
     any(any(element != 0 for element in row[0 : block_len]) for row in matrix[block_len : ]):
    raise ValueError("Matrix should be block-diagonal")

  a = [row[0 : block_len] for row in matrix[0 : block_len]]
  b = [row[block_len : ] for row in matrix[block_len : ]]
  return (a, b)
