import pytest
from qsharp import init, eval

test_cases = [
      (2, [0]),
      (2, [1]),
      (3, [0, 3]),
      (3, [1, 4]),
      (3, [2, 7])
    ]

@pytest.mark.parametrize("n, markedStates", test_cases)
def test_grovers_search(n, markedStates):
  init(project_root='.')
  # Run Grover's search end-to-end and check that 
  # the result is the big endian representation of one of the marked states 100% of the time
  n_runs = 100
  n_correct = 0
  for _ in range(n_runs):
    resBits = eval("GroversSearch.RunGroversSearch(" +
       f"{n}, GroversSearch.MarkStates(_, _, {markedStates}), ApplyToEachA(H, _), 1)")
    resStr = "".join(["1" if b else "0" for b in resBits])
    resInt = int(resStr, 2)
    if resInt in markedStates:
      n_correct += 1
  assert n_correct == n_runs