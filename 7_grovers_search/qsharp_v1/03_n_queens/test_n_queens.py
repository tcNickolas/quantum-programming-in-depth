import pytest
from qsharp import init, eval

@pytest.mark.parametrize("n, mode", [
  (4, "Bits"), 
  (5, "Bits"),
  (4, "Indices"), 
  (5, "Indices"),
  ])
def test_nqueens(n, mode):
  init(project_root='.')
  eval(f"NQueens.Test.AssertOracleIsValid({n}, NQueens.Test.IntAsEncoding_{mode}, NQueens.NQueensOracle_{mode}, NQueens.Test.IsEncodingValid_{mode})")
