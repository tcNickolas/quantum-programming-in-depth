import pytest
from qsharp import init, eval

@pytest.mark.parametrize("op", ["Zero", "One", "X", "OneMinusX"])
def test_single_bit_function(op):
  init(project_root='.')
  eval("ReversibleComputing.Test.AssertOperationImplementsFunction(" +
       f"ReversibleComputing.Quantum{op}, ReversibleComputing.Test.F{op})")
