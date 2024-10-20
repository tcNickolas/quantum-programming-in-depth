from qiskit import QuantumCircuit

def distinguish_x_z(unitary_circ):
  circ = QuantumCircuit(1, 1)
  circ.append(unitary_circ, [0])
  circ.x(0)
  circ.measure(0, 0)
  return circ

def distinguish_x_h(unitary_circ):
  circ = QuantumCircuit(1, 1)
  circ.append(unitary_circ, [0])
  circ.x(0)
  circ.append(unitary_circ, [0])
  circ.x(0)
  circ.measure(0, 0)
  return circ

def distinguish_x_minusx(unitary_circ):
  circ = QuantumCircuit(2, 1)
  circ.h(0)
  circ.h(1)
  circ.append(unitary_circ.to_gate().control(1), [0, 1])
  circ.h(0)
  circ.h(1)
  circ.measure(0, 0)
  return circ
