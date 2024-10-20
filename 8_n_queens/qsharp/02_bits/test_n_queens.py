import pytest
from qsharp import init, eval

@pytest.mark.parametrize("n", [4, 5])
def test_nqueens(n):
  init(project_root='.')
  eval(f"NQueens.Test.AssertOracleIsValid({n}, NQueens.Test.IntAsEncoding_Bits, NQueens.Oracle_Bits, NQueens.Test.IsPlacementValid_Bits)")
