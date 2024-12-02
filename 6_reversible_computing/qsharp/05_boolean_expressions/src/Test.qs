import Std.Convert.IntAsBoolArray;
import Std.Diagnostics.CheckAllZero;

operation AssertOperationImplementsFunction(
  N : Int, 
  op : (Qubit[], Qubit) => Unit, 
  f : Bool[] -> Bool
) : Unit {
  use (x, y) = (Qubit[N], Qubit());
  for input in 0 .. (1 <<< N) - 1 {
    let inBits = IntAsBoolArray(input, N);
    ApplyPauliFromBitString(PauliX, true, inBits, x);

    op(x, y);

    let expected = f(inBits);
    if expected {
      X(y);
    }

    ApplyPauliFromBitString(PauliX, true, inBits, x);

    if not CheckAllZero([y]) {
      fail $"Error for x={inBits}: expected {expected}, got {not expected}";
    }
    if not CheckAllZero(x) {
      fail $"Error for x={inBits}: the state of input qubits was modified";
    }
  }
}


function FEvaluateClause(args: Bool[], literals : (Int, Bool)[]) : Bool {
  for (ind, pos) in literals {
    if pos and args[ind] or not pos and not args[ind] {
      return true;
    }
  }
  return false;
}


function FEvaluateExpression(args: Bool[], expression : (Int, Bool)[][]) : Bool {
  for clause in expression {
    if not FEvaluateClause(args, clause) {
      return false;
    }
  }
  return true;
}
