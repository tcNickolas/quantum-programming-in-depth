from cmath import isclose
from .boolean_expressions import evaluate_clause, evaluate_formula
import pytest
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from functools import partial

def f_evaluate_clause(args, literals):
  for (ind, pos) in literals:
    if pos and args[ind] or not pos and not args[ind]:
      return True
  return False

def f_evaluate_formula(args, formula):
  for clause in formula:
    if not f_evaluate_clause(args, clause):
      return False
  return True


simulator = Aer.get_backend('aer_simulator')

def run_test_oracle(n_inputs, n_qubits, oracle, function):
  format_str = f"{{:0>{n_inputs}b}}"
  for input in range(2 ** n_inputs):
    input_str = format_str.format(input)
    input_be = [input_str[i] == '1' for i in range(n_inputs)]

    circ = QuantumCircuit(n_qubits)
    for i in range(n_inputs):
      if input_be[i]:
        circ.x(i)

    circ.append(oracle(n_inputs), range(n_qubits))

    expected = function(input_be)
    if expected:
      circ.x(n_qubits - 1)

    for i in range(n_inputs):
      if input_be[i]:
        circ.x(i)

    circ = circ.decompose(reps=4)
    circ.save_statevector()

    res = simulator.run(circ).result()
    state_vector = res.get_statevector().data

    non_zeros = [not isclose(amp, 0, abs_tol=1e-9) for amp in state_vector]
    if any(non_zeros[1:]):
      # Either result is incorrect or inputs are modified.
      # Result is stored in most significant bit, input - in least significant bit
      count = non_zeros.count(True)
      if count > 1:
        raise Exception(f"Unexpected result for input {input}: the state should not be a superposition")

      index = non_zeros.index(True)
      if index // (2 ** (n_qubits - 1)) > 0:
        raise Exception(f"Unexpected result for input {input}: expected {expected}, got {not expected}")
      else:
        raise Exception(f"Unexpected result for input {input}: the state of the input qubits was modified")



@pytest.mark.parametrize("n, clause", 
    [
      (1, []),
      (1, [(0, True)]),
      (1, [(0, False)]),
      (2, [(0, True), (1, True)]),
      (2, [(0, False), (1, True)]),
      (3, [(1, False), (2, False)])
    ])
def test_evaluate_clause(n, clause):
  oracle = partial(evaluate_clause, literals=clause)
  function = partial(f_evaluate_clause, literals=clause)
  run_test_oracle(n, n + 1, oracle, function)


@pytest.mark.parametrize("n, formula", 
    [
      (1, [[(0, True)], [(0, False)]]), # 0 solutions
      (1, [[(0, False)]]),              # 1 solution
      (1, []),                          # 2 solutions
      (2, [[(0, True)], [(1, True)]]),  # 1 solution
      (2, [[(0, False), (1, False)], [(0, True), (1, True)]]), # 2 solutions
      (2, [[(0, False), (1, False)]]),  # 3 solutions
      (3, [[(2, False), (1, True)], [(2, True), (1, False)]]), # 4 solutions
    ])
def test_evaluate_formula(n, formula):
  oracle = partial(evaluate_formula, formula=formula)
  function = partial(f_evaluate_formula, formula=formula)
  run_test_oracle(n, n + len(formula) + 1, oracle, function)
