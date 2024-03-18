from cmath import exp, isclose, pi
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

simulator = Aer.get_backend('aer_simulator')

def z_gate():
  circ = QuantumCircuit(1)
  circ.z(0)
  return circ

def inc_gate():
  circ = QuantumCircuit(2)
  circ.cx(0, 1)
  circ.x(0)
  return circ.to_gate()

def t_gate():
  circ = QuantumCircuit(1)
  circ.t(0)
  return circ.to_gate()

z_eigenvectors = [[1, 0], [0, 1]]

inc_eigenvectors = [
    [0.5, 0.5, 0.5, 0.5],
    [0.5, -0.5, 0.5, -0.5],
    [0.5, -0.5j, -0.5, 0.5j],
    [0.5, 0.5j, -0.5, -0.5j]
  ]

z_eigenphases = [0, 0.5]

inc_eigenphases = [0.0, 0.5, 0.25, 0.75]

t_eigenphases = [0, 0.125]


def test_validate_inputs():
  for (n_qubits, n_eigenvectors, unitary, eigenvectors, eigenphases) in [
    (1, 2, z_gate(), z_eigenvectors, z_eigenphases),
    (2, 4, inc_gate(), inc_eigenvectors, inc_eigenphases),
    (1, 2, t_gate(), z_eigenvectors, t_eigenphases)
  ]:
    for ind in range(n_eigenvectors):
      circ = QuantumCircuit(n_qubits)
      circ.initialize(eigenvectors[ind])
      circ.append(unitary, range(n_qubits))
      circ = transpile(circ, backend=simulator)
      circ.save_statevector()

      res = simulator.run(circ).result()
      state_vector = res.get_statevector().data
      exp_vector = [amp * exp(2 * 1j * pi * eigenphases[ind]) for amp in eigenvectors[ind]]
      for (actual, expected) in zip(state_vector, exp_vector):
        assert isclose(actual, expected)
