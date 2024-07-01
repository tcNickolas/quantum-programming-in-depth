import qsharp

def test_state_parity():
  qsharp.init(project_root='.')
  qsharp.eval("AnalyzeStates.Test.TestStateParity()")
