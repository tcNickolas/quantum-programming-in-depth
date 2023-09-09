from math import atan2, sqrt
from qiskit import QuantumCircuit

def prep_one_qubit(alpha, beta):
  circ = QuantumCircuit(1, name=f'Prep({alpha}, {beta})')
  theta = atan2(beta, alpha)
  circ.ry(2 * theta, 0)
  return circ.to_gate()

def prep_multi_qubit(n, a):
  circ = QuantumCircuit(n)

  if n == 1:
    circ.append(prep_one_qubit(a[0], a[1]), [0])
    return circ
    
  zero_amps = a[0 : : 2]
  one_amps = a[1 : : 2]

  m0 = sqrt(sum(a*a for a in zero_amps))
  m1 = sqrt(sum(a*a for a in one_amps))

  circ.append(prep_one_qubit(m0, m1), [0])

  circ.append(prep_multi_qubit(n - 1, zero_amps)
              .to_gate().control(1, ctrl_state=0), range(n))

  circ.append(prep_multi_qubit(n - 1, one_amps)
              .to_gate().control(1), range(n))

  return circ
