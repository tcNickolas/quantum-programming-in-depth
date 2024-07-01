import pytest
import qsharp

@pytest.mark.parametrize("gates,op", 
    [
      ("X, Z", "AnalyzeUnitaries.DistinguishXZ"),
      ("X, H", "AnalyzeUnitaries.DistinguishXH"),
      ("X, AnalyzeUnitaries.Test.MinusX", "AnalyzeUnitaries.DistinguishXMinusX")
    ])
def test_distinguish_gates(gates, op):
  qsharp.init(project_root='.')
  qsharp.eval(f"AnalyzeUnitaries.Test.DistinguishTwoGatesTestLogic([{gates}], {op})")
