namespace ReversibleComputing.Test {
  open Microsoft.Quantum.Logical;
  open Microsoft.Quantum.Convert;
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Diagnostics;
  open ReversibleComputing;

  operation AssertMarkingOracleImplementsFunction(
    N : Int, 
    oracle : (Qubit[], Qubit) => Unit, 
    f : Bool[] -> Bool
  ) : Unit {
    use (x, y) = (Qubit[N], Qubit());
    for input in 0 .. (1 <<< N) - 1 {
      let inputBE = Reversed(IntAsBoolArray(input, N));
      ApplyPauliFromBitString(PauliX, true, inputBE, x);

      oracle(x, y);

      let expected = f(inputBE);
      if expected {
        X(y);
      }

      if not CheckAllZero([y]) {
        fail $"Unexpected result for input {inputBE}: expected {expected}, got {not expected}";
      }

      ApplyPauliFromBitString(PauliX, true, inputBE, x);
      if not CheckAllZero(x) {
        fail $"Unexpected behavior for input {inputBE}: the state of input qubits was modified";
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


  function FEvaluateFormula(args: Bool[], formula : (Int, Bool)[][]) : Bool {
    for clause in formula {
      if not FEvaluateClause(args, clause) {
        return false;
      }
    }
    return true;
  }
}