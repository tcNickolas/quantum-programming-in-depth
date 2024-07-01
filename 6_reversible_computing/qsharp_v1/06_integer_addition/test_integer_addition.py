import pytest
from qsharp import init, eval

@pytest.mark.parametrize("n", [1, 2, 3, 4, 5])
def test_adder(n):
  init(project_root='.')
  eval(f"ReversibleComputing.Test.TestAdder({n})")
