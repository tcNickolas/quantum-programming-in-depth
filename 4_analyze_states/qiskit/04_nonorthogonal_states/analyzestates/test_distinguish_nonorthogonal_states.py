from .distinguish_nonorthogonal_states import distinguish_zero_and_sup
from math import atan2, cos, pi, sin
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from random import uniform

def prep_input_state(alpha, beta, ind):
  circ = QuantumCircuit(1)
  if ind == 1:
    circ.ry(2. * atan2(beta, alpha), 0)
  return circ

simulator = Aer.get_backend('aer_simulator')

def test_distinguish_zero_and_sup():
  for _ in range(10):
    angle = uniform(0, pi / 2)
    (alpha, beta) = (cos(angle), sin(angle))
    n_correct = 0
    n_trials_each = 1000
    for state_ind in range(2):
      circ = QuantumCircuit(1, 1)
      circ.append(prep_input_state(alpha, beta, state_ind), [0])
      circ.append(distinguish_zero_and_sup(alpha, beta), [0], [0])

      circ = transpile(circ, backend=simulator)
      res_map = simulator.run(circ, shots=n_trials_each).result().get_counts()
      # The number of correct guesses is the map element with key equal to state_ind
      n_correct += res_map[str(state_ind)]

    p_success = n_correct / (2 * n_trials_each)
    p_success_theor = 0.5 * (1 + beta)

    print(f"Correct guesses {p_success}, theoretical {p_success_theor}")
    assert abs(p_success - p_success_theor) < 0.05
