from qsharp import eval, init
from qsharp.utils import dump_operation
import pytest

test_cases = [
      (1, []),
      (1, [1]),
      (2, [1]),
      (2, [2]),
      (2, [0, 3]),
      (3, [0, 3, 6]),
      (3, [1, 3, 5, 7])
    ]


@pytest.mark.parametrize("n, marked_states", test_cases)
def test_mark_states(n, marked_states):
  init(project_root='.')
  eval("Test.AssertOperationImplementsFunction(" +
       f"{n}, Oracles.MarkStates(_, _, {marked_states}), " + 
       f"Test.FMarkStates(_, {marked_states}))")


@pytest.mark.parametrize("n, marked_states", test_cases)
def test_apply_phase_oracle(n, marked_states):
  init(project_root='.')
  matrix = dump_operation(f"Oracles.ApplyPhaseOracle(_, Oracles.MarkStates(_, _, {marked_states}))", n)

  complete_coef = []
  for state in range(2 ** n):
    row = [0] * (2 ** n)
    row[state] = -1 if state in marked_states else 1
    complete_coef += [row]

  for actual, expected in zip(matrix, complete_coef):
    assert actual == pytest.approx(expected, abs=1e-6)
