import qsharp

def test_distinguish_states():
  qsharp.init(project_root='.')
  qsharp.eval("Test.TestDistinguishStates()")
