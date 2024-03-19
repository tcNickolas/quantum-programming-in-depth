import qsharp

def test_reconstruct_unitary():
  qsharp.init(project_root='.')
  qsharp.eval("AnalyzeUnitaries.Test.TestReconstructUnitary()")
