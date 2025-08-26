from math import atan2, pi, sqrt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

simulator = AerSimulator(method='statevector')

def reconstruct_state(state_prep):
  # Figure out the absolute values of alpha and beta
  circ1 = QuantumCircuit(1, 1)
  circ1.append(state_prep, [0])
  circ1.measure(0, 0)
  circ1 = transpile(circ1, backend=simulator)

  n_trials = 200
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


def reconstruct_unitary(gate):
  # Analyze the effects of the gate on the |0> state to get the first column
  (a, b) = reconstruct_state(gate)
  # Figure out whether the second column is (b; -a) or (-b; a)
  # Prepare a state a|0> + b|1> and apply the unitary to it; 
  # in the first case, the result is always |0>, in the second case, (a^2-b^2)|0> + 2ab|1>
  circ = QuantumCircuit(1, 1)
  # Prepare a state a|0> + b|1> using the unitary itself and apply the unitary to it again
  circ.append(gate, [0])
  circ.append(gate, [0])
  if b < 0:
    circ.z(0)
  # Treat the result as a choice between |0> and (a^2-b^2)|0> + 2ab|1>
  # Figure out the angle of the line halfway between |0> and alpha |0> + beta |1>
  theta = atan2(2 * a * abs(b), a * a - b * b) / 2
  # Rotate so that the middle between the two angles is at the angle pi/4
  circ.ry(- 2 * (theta - pi / 4), [0])
  circ.measure(0, 0)
  circ = transpile(circ, backend=simulator)

  n_trials = 200
  res_map = simulator.run(circ, shots=n_trials).result().get_counts()
  if '0' in res_map and 2 * res_map['0'] > n_trials:
    return [[a, b], [b, -a]]
  else:
    return [[a, -b], [b, a]]
