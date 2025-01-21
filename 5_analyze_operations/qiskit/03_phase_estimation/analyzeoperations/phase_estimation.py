from math import acos, pi, sqrt
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library.standard_gates import SdgGate
from qiskit_aer import AerSimulator

simulator = AerSimulator(method='statevector')

def one_bit_phase_estimation(n, eigenvector, unitary):
  circ = QuantumCircuit(n + 1, 1)
  circ.h(0)
  eig = range(1, n + 1)
  circ.initialize(eigenvector, eig)
  circ.append(unitary.control(1), [0] + list(eig))
  circ.h(0)
  circ.measure(0, 0)
  circ = transpile(circ, backend=simulator)

  res_map = simulator.run(circ, shots=1).result().get_counts()
  res_int = int(list(res_map.keys())[0], 2)
  return res_int * 0.5


def iterative_phase_estimation(n, eigenvector, unitary):
  circ = QuantumCircuit(n + 1, 1)
  circ.h(0)
  eig = range(1, n + 1)
  circ.initialize(eigenvector, eig)
  circ.append(unitary.control(1), [0] + list(eig))
  circ.h(0)
  circ.measure(0, 0)
  circ = transpile(circ, backend=simulator)

  n_trials = 10000
  res_map = simulator.run(circ, shots=n_trials).result().get_counts()
  n_zeros = res_map['0'] if '0' in res_map else 0
  return acos(sqrt(n_zeros / n_trials)) / pi


def two_bit_adaptive_phase_estimation(n, eigenvector, unitary):
  res_bits = [0, 0]
  # Estimate the least significant bit
  circ = QuantumCircuit(n + 1, 1)
  circ.h(0)
  eig = range(1, n + 1)
  circ.initialize(eigenvector, eig)
  circ.append(unitary.control(1), [0] + list(eig))
  circ.append(unitary.control(1), [0] + list(eig))
  circ.h(0)
  circ.measure(0, 0)
  circ = transpile(circ, backend=simulator)
  res_map = simulator.run(circ).result().get_counts()
  res_bits[1] = int(list(res_map.keys())[0], 2)

  # Estimate the most significant bit
  circ = QuantumCircuit(n + 1, 1)
  circ.h(0)
  eig = range(1, n + 1)
  circ.initialize(eigenvector, eig)
  circ.append(unitary.control(1), [0] + list(eig))
  if res_bits[1] == 1:
    circ.sdg(0)
  circ.h(0)
  circ.measure(0, 0)
  circ = transpile(circ, backend=simulator)
  res_map = simulator.run(circ).result().get_counts()
  res_bits[0] = int(list(res_map.keys())[0], 2)

  return (res_bits[0] * 2 + res_bits[1]) / 4


def two_bit_quantum_phase_estimation(n, eigenvector, unitary):
  circ = QuantumCircuit(n + 2, 2)
  circ.h(0)
  circ.h(1)
  eig = range(2, n + 2)
  circ.initialize(eigenvector, eig)
  circ.append(unitary.control(1), [1] + list(eig))
  circ.append(unitary.control(1), [0] + list(eig))
  circ.append(unitary.control(1), [0] + list(eig))
  # Inverse QFT for 2 bits
  circ.swap(0, 1)
  circ.h(1)
  circ.append(SdgGate().control(1), [1, 0])
  circ.h(0)
  circ.measure([0, 1], [0, 1])
  circ = transpile(circ, backend=simulator)
  res_map = simulator.run(circ).result().get_counts()
  return int(list(res_map.keys())[0][::-1], 2) / 4
