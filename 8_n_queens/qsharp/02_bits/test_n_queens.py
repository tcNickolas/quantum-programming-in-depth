import pytest
from qsharp import init, eval

@pytest.mark.parametrize("n", [4, 5])
def test_nqueens(n):
  init(project_root='.')
  eval(f"Test.AssertOracleIsValid({n}, Test.IntAsEncoding_Bits, NQueens.Oracle_Bits, Test.IsPlacementValid_Bits)")
