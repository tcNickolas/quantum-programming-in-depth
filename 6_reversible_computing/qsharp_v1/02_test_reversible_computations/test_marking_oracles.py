import pytest
from qsharp import init, eval

@pytest.mark.parametrize("op", 
    [
      ("Zero"),
      ("One"),
      ("X")
    ])
def test_marking_oracle(op):
  init(project_root='.')
  eval("ReversibleComputing.Test.AssertMarkingOracleImplementsFunction(" +
       f"ReversibleComputing.Oracle{op}, ReversibleComputing.Test.F{op})")
