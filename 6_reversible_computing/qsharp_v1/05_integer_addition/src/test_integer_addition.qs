namespace ReversibleComputing.Test {
  open Microsoft.Quantum.Logical;
  open Microsoft.Quantum.Convert;
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Diagnostics;
  open ReversibleComputing;

  operation TestAdder(
    N : Int
  ) : Unit {
    use (a, b, sum) = (Qubit[N], Qubit[N], Qubit[N]);
    for aInt in 0 .. (1 <<< N) - 1 {
      for bInt in 0 .. (1 <<< N) - 1 {
        let sumInt = (aInt + bInt) % (1 <<< N);
        let aBE = Reversed(IntAsBoolArray(aInt, N));
        let bBE = Reversed(IntAsBoolArray(bInt, N));
        let sumBE = Reversed(IntAsBoolArray(sumInt, N));

        within {
          ApplyPauliFromBitString(PauliX, true, aBE, a);
          ApplyPauliFromBitString(PauliX, true, bBE, b);
        } apply {
          Adder(a, b, sum);

          // Check that sum is correct
          ApplyPauliFromBitString(PauliX, true, sumBE, sum);
          if not CheckAllZero(sum) {
            fail $"Unexpected result for a={a}, b={b}: expected {sum}, got the following state:";
            ApplyPauliFromBitString(PauliX, true, sumBE, sum);
            DumpRegister(sum);
          }
        }

        // Check that inputs are unchanged
        if not CheckAllZero(a + b) {
          fail $"Unexpected behavior for a={a}, b={b}: the state of input qubits was modified";
        }
      }
    }
  }
}