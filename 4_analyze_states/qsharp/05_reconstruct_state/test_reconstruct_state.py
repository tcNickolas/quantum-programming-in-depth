import qsharp

def test_reconstruct_state():
  qsharp.init(project_root='.')
  qsharp.eval("AnalyzeStates.Test.TestReconstructState()")
