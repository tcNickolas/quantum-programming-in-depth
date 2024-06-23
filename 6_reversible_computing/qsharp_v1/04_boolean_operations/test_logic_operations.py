import pytest
from qsharp import init, eval

@pytest.mark.parametrize("n, op", 
    [
      (1, "Negation"),
      (2, "Xor"),
      (2, "And"),
      (2, "Or"),
      (2, "Equality"),
      (2, "MultiAnd"),
      (3, "MultiAnd"),
      (2, "MultiOr"),
      (3, "MultiOr")
    ])
def test_logic_operation(n, op):
  init(project_root='.')
  eval("ReversibleComputing.Test.AssertMarkingOracleImplementsFunction(" +
       f"{n}, ReversibleComputing.{op}, ReversibleComputing.Test.F{op})")
