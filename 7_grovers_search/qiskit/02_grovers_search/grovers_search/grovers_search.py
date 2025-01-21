from qiskit import QuantumCircuit
from qiskit.circuit.library.standard_gates import XGate, ZGate

def mark_states(n, marked_states):
  circ = QuantumCircuit(n + 1)
  for state in marked_states:
    # Reverse control bit string, since controls use little endian
    stateBE = (f"{{:0>{n}b}}".format(state))[::-1]
    circ.append(XGate().control(n, ctrl_state=stateBE), range(n + 1))
  return circ


def phase_oracle(n, marking_oracle):
  circ = QuantumCircuit(n + 1)
  circ.h(n)
  circ.z(n)
  circ.append(marking_oracle.to_gate(), range(n + 1))
  circ.z(n)
  circ.h(n)
  return circ.to_gate()


def grovers_search(n_bits, marking_oracle, prepare_mean, n_iterations):
  # Define Grover's iteration
  iter = QuantumCircuit(n_bits + 1)
  # Apply phase oracle
  phase_or = phase_oracle(n_bits, marking_oracle)
  iter.append(phase_or, range(n_bits + 1))
  # Apply reflection about the mean
  iter.append(prepare_mean.inverse(), range(n_bits))
  iter.x(range(n_bits))
  iter.append(ZGate().control(n_bits - 1), range(n_bits))
  iter.x(range(n_bits))
  iter.append(prepare_mean, range(n_bits))

  circ = QuantumCircuit(n_bits + 1, n_bits)
  circ.append(prepare_mean, range(n_bits))
  circ.append(iter.to_gate().power(n_iterations), range(n_bits + 1))
  circ.measure(range(n_bits), range(n_bits))

  return circ
