from math import pi, sqrt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

simulator = AerSimulator(method='statevector')

def reconstruct_state(state_prep):
  # Figure out the absolute values of alpha and beta
  circ1 = QuantumCircuit(1, 1)
  circ1.append(state_prep, [0])
  circ1.measure(0, 0)
  circ1 = transpile(circ1, backend=simulator)

  n_trials = 1000
  res_map = simulator.run(circ1, shots=n_trials).result().get_counts()
  if '0' in res_map:
    (n0, n1) = (res_map['0'], n_trials - res_map['0'])
  else:
    (n0, n1) = (n_trials - res_map['1'], res_map['1'])
  alpha = sqrt(n0 / n_trials)
  beta = sqrt(n1 / n_trials)

  # Figure out whether there is a relative phase of -1
  # (distinguish alpha |0> + beta |1> from alpha |0> - beta |1>).
  # The mid-line between them would be horizontal, so we rotate by PI/4 clockwise
  circ2 = QuantumCircuit(1, 1)
  circ2.append(state_prep, [0])
  circ2.ry(pi / 2, 0)
  circ2.measure(0, 0)
  circ2 = transpile(circ2, backend=simulator)

  res_map = simulator.run(circ2, shots=n_trials).result().get_counts()
  if '0' in res_map and 2 * res_map['0'] > n_trials:
    return (alpha, -beta)
  else:
    return (alpha, beta)
