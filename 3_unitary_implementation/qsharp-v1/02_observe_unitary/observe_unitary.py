import qsharp
import qsharp.utils

coef = [[0.6, -0.8], [0.8, 0.6]]

qsharp.init(project_root='.')
print(qsharp.utils.dump_operation(f"UnitaryImplementation.ApplyOneQubit(_, {coef})", 1))
