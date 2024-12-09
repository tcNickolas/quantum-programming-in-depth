import qsharp
import pytest

@pytest.mark.parametrize("gates,op", 
    [
      ("X, Z", "AnalyzeUnitaries.DistinguishXZ"),
      ("X, H", "AnalyzeUnitaries.DistinguishXH"),
      ("X, Test.MinusX", "AnalyzeUnitaries.DistinguishXMinusX")
    ])
def test_distinguish_gates(gates, op):
  qsharp.init(project_root='.')
  qsharp.eval(f"Test.DistinguishTwoGatesTestLogic([{gates}], {op})")
