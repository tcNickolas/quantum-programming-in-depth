from qsharp import eval, init
import pytest

@pytest.mark.parametrize("n", [4, 5])
def test_nqueens(n):
  init(project_root='.')
  eval(f"Test.AssertOracleIsValid({n}, Test.IntAsEncoding_Indices, NQueens.Oracle_Indices, Test.IsPlacementValid_Indices)")
