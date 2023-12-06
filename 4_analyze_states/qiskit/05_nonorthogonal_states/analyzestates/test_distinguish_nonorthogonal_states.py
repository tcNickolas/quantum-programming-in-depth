from .distinguish_nonorthogonal_states import distinguish_zero_and_sup
from math import atan2, cos, pi, sin, sqrt
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from random import randrange, uniform

def prep_input_state(alpha, beta, ind):
  circ = QuantumCircuit(1)
  if ind == 1:
    circ.ry(2. * atan2(beta, alpha), 0)
  return circ

def test_distinguish_zero_and_sup():
  for _ in range(10):
    angle = uniform(0, pi / 2)
    (alpha, beta) = (cos(angle), sin(angle))
    n_correct = 0
    n_trials = 1000
    for _ in range(n_trials):
      state_ind = randrange(0, 2)

      circ = QuantumCircuit(1, 1)
      circ.append(prep_input_state(alpha, beta, state_ind), [0])
      circ.append(distinguish_zero_and_sup(alpha, beta), [0], [0])
      circ = circ.decompose()

      simulator = Aer.get_backend('aer_simulator')
      res_map = simulator.run(circ, shots=1).result().get_counts()
      res_state = int(list(res_map.keys())[0], 2)
      
      if state_ind == res_state:
        n_correct += 1

    p_success = n_correct / n_trials
    p_success_theor = 0.5 * (1 + sqrt(1 - alpha ** 2))

    print(f"Correct guesses {p_success}, theoretical {p_success_theor}")
    assert abs(p_success - p_success_theor) < 0.05
