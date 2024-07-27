namespace NQueens.Test {
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Convert;
  open Microsoft.Quantum.Diagnostics;
  open NQueens;

  operation AssertOracleIsValid(
    n : Int
  ) : Unit {
    use (x, y) = (Qubit[n * n], Qubit());
    // Limit the consideration to placements with one queen per row
    for indicesInt in 0 .. n ^ n - 1 {
      mutable current = indicesInt;
      mutable bits = [false, size = n * n];
      for row in 0 .. n - 1 {
        set bits w/= row * n + (current % n) <- true;
        set current /= n;
      }
      ApplyPauliFromBitString(PauliX, true, bits, x);
      NQueensOracle(n, x, y);
      ApplyPauliFromBitString(PauliX, true, bits, x);

      let expected = IsArrangementValid(n, bits);
      if expected {
        X(y);
      }

      if not CheckAllZero([y]) {
        fail $"Error for x={bits}: expected {expected}, got {not expected}";
      }
      if not CheckAllZero(x) {
        fail $"Error for x={bits}: the state of input qubits was modified";
      }
    }
  }


  function IsArrangementValid(n : Int, bits: Bool[]) : Bool {
    let board = Chunks(n, bits);
    // One queen per row
    for r in 0 .. n - 1 {
      let nQ = Count(x -> x, board[r]);
      if nQ != 1 {
        // Message($"Row {r} has {nQ} queens");
        return false;
      }
    }
    // One queen per column
    for c in 0 .. n - 1 {
      let nQ = Count(x -> x, Mapped(row -> row[c], board));
      if nQ != 1 {
        // Message($"Column {c} has {nQ} queens");
        return false;
      }
    }
    // One queen per diagonal
    for r1 in 0 .. n - 1 {
      for r2 in r1 + 1 .. n - 1 {
        for c1 in 0 .. n - 1 {
          for c2 in [c1 + r2 - r1, c1 - r2 + r1] {
            if c2 >= 0 and c2 < n and board[r1][c1] and board[r2][c2] {
              // Message($"Queens ({r1}, {c1}) and ({r2}, {c2}) on diagonal");
              return false;
            }
          }
        }
      }
    }
    return true;
  }
}