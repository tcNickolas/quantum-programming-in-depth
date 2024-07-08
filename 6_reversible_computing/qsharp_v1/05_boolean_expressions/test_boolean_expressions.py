import pytest
from qsharp import init, eval

@pytest.mark.parametrize("n, clause", 
    [
      (1, "[]"),
      (1, "[(0, true)]"),
      (1, "[(0, false)]"),
      (2, "[(0, true), (1, true)]"),
      (2, "[(0, false), (1, true)]"),
      (3, "[(1, false), (2, false)]")
    ])
def test_evaluate_clause(n, clause):
  init(project_root='.')
  eval("ReversibleComputing.Test.AssertOperationImplementsFunction(" +
       f"{n}, ReversibleComputing.EvaluateClause(_, _, {clause}), " + 
       f"ReversibleComputing.Test.FEvaluateClause(_, {clause}))")


@pytest.mark.parametrize("n, expression", 
    [
      (1, "[[(0, true)], [(0, false)]]"), # 0 solutions
      (1, "[[(0, false)]]"),              # 1 solution
      (1, "[]"),                          # 2 solutions
      (2, "[[(0, true)], [(1, true)]]"),  # 1 solution
      (2, "[[(0, false), (1, false)], [(0, true), (1, true)]]"), # 2 solutions
      (2, "[[(0, false), (1, false)]]"),  # 3 solutions
      (3, "[[(2, false), (1, true)], [(2, true), (1, false)]]"), # 4 solutions
    ])
def test_evaluate_expression(n, expression):
  init(project_root='.')
  eval("ReversibleComputing.Test.AssertOperationImplementsFunction(" +
       f"{n}, ReversibleComputing.EvaluateExpression(_, _, {expression}), " +
       f"ReversibleComputing.Test.FEvaluateExpression(_, {expression}))")
