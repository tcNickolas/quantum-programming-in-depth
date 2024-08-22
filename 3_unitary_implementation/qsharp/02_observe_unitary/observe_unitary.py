import qsharp
from qsharp.utils import dump_operation

coef = [[0.6, -0.8], [0.8, 0.6]]

qsharp.init(project_root='.')
print(dump_operation(f"UnitaryImplementation.ApplyOneQubit(_, {coef})", 1))
