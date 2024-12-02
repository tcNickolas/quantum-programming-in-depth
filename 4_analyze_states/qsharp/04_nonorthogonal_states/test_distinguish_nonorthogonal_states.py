import qsharp

def test_distinguish_nonorthogonal_states():
  qsharp.init(project_root='.')
  qsharp.eval("Test.TestDistinguishZeroAndSup()")
