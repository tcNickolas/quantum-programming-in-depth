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


  function FNegation(args: Bool[]) : Bool {
    return not args[0];
  }


  function FXor(args: Bool[]) : Bool {
    return args[0] != args[1];
  }


  function FAnd(args: Bool[]) : Bool {
    return args[0] and args[1];
  }


  function FOr(args: Bool[]) : Bool {
    return args[0] or args[1];
  }


  function FEquality(args: Bool[]) : Bool {
    return args[0] == args[1];
  }


  function FMultiAnd(args: Bool[]) : Bool {
    return All(a -> a, args);
  }


  function FMultiOr(args: Bool[]) : Bool {
    return Any(a -> a, args);
  }
}