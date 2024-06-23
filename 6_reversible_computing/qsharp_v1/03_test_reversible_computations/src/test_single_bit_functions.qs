namespace ReversibleComputing.Test {
  open Microsoft.Quantum.Logical;
  open Microsoft.Quantum.Convert;
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Diagnostics;
  open ReversibleComputing;

  operation AssertMarkingOracleImplementsFunction(
    oracle : (Qubit, Qubit) => Unit, 
    f : Bool -> Bool
  ) : Unit {
    use (x, y) = (Qubit(), Qubit());
    for input in [false, true] {
      if input {
        X(x);
      }

      oracle(x, y);

      let expected = f(input);
      if expected {
        X(y);
      }

      if not CheckAllZero([y]) {
        fail $"Unexpected result for input {input}: expected {expected}, got {not expected}";
      }

      if input {
        X(x);
      }
      if not CheckAllZero([x]) {
        fail $"Unexpected behavior for input {input}: the state of the input qubit was modified";
      }
    }
  }


  function FZero(arg : Bool) : Bool {
    return false;
  }


  function FOne(arg : Bool) : Bool {
    return true;
  }


  function FX(arg : Bool) : Bool {
    return arg;
  }
}