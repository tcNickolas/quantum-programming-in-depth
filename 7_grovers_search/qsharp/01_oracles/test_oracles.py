import pytest
from qsharp import init, eval
from qsharp.utils import dump_operation

test_cases = [
      (1, []),
      (1, [1]),
      (2, [1]),
      (2, [2]),
      (2, [0, 3]),
      (3, [0, 3, 6]),
      (3, [1, 3, 5, 7])
    ]


@pytest.mark.parametrize("n, markedStates", test_cases)
def test_mark_states(n, markedStates):
  init(project_root='.')
  eval("GroversSearch.Test.AssertOperationImplementsFunction(" +
       f"{n}, GroversSearch.MarkStates(_, _, {markedStates}), " + 
       f"GroversSearch.Test.FMarkStates(_, {markedStates}))")


@pytest.mark.parametrize("n, marked_states", test_cases)
def test_apply_phase_oracle(n, marked_states):
  init(project_root='.')
  matrix = dump_operation(f"GroversSearch.ApplyPhaseOracle(_, GroversSearch.MarkStates(_, _, {markedStates}))", n)

  complete_coef = []
  for state in range(2 ** n):
    row = [0] * (2 ** n)
    row[state] = -1 if state in marked_states else 1
    complete_coef += [row]

  for actual, expected in zip(matrix, complete_coef):
    assert actual == pytest.approx(expected, abs=1e-6)
