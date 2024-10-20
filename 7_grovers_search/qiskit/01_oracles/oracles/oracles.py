from qiskit import QuantumCircuit
from qiskit.circuit.library.standard_gates import XGate

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
  circ.append(marking_oracle, range(n + 1))
  circ.z(n)
  circ.h(n)
  return circ