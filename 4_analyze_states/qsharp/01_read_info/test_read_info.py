import qsharp

def test_read_info():
  qsharp.init(project_root='.')
  qsharp.eval("Test.TestReadInformation()")
