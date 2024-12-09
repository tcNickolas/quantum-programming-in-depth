from qsharp import eval, init
import pytest

@pytest.mark.parametrize("op", ["Zero", "One", "X", "OneMinusX"])
def test_single_bit_function(op):
  init(project_root='.')
  eval("Test.AssertOperationImplementsFunction(" +
       f"ReversibleComputing.Quantum{op}, Test.F{op})")
