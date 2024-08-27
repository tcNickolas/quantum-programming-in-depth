namespace NQueens.Test {
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Convert;
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Math;
  open NQueens;

  operation AssertOracleIsValid(
    n : Int,
    intAsEncoding : (Int, Int) -> Bool[],
    oracle : (Int, Qubit[], Qubit) => Unit,
    isEncodingValid : (Int, Bool[]) -> Bool
  ) : Unit {
    // Limit the consideration to placements with one queen per row
    for indicesInt in 0 .. n ^ n - 1 {
      let bits = intAsEncoding(n, indicesInt);
      use (x, y) = (Qubit[Length(bits)], Qubit());
      ApplyPauliFromBitString(PauliX, true, bits, x);
      oracle(n, x, y);
      ApplyPauliFromBitString(PauliX, true, bits, x);

      let expected = isEncodingValid(n, bits);
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

  function IntAsEncoding_Bits(n : Int, int : Int) : Bool[] {
    mutable current = int;
    mutable bits = [false, size = n * n];
    for row in 0 .. n - 1 {
      set bits w/= row * n + (current % n) <- true;
      set current /= n;
    }
    return bits;
  }

  function IntAsEncoding_Indices(n : Int, int : Int) : Bool[] {
    mutable current = int;
    let bitSize = BitSizeI(n - 1);
    mutable bits = [];
    for _ in 0 .. n - 1 {
      // Use big endian
      set bits += Reversed(IntAsBoolArray(current % n, bitSize));
      set current /= n;
    }
    return bits;
  }

  function IsEncodingValid_Bits(n : Int, bits: Bool[]) : Bool {
    let board = Chunks(n, bits);
    // One queen per row
    for r in 0 .. n - 1 {
      let nQ = Count(x -> x, board[r]);
      if nQ != 1 {
        // Message($"Row {r} has {nQ} queens");
        return false;
      }
    }
    let indices = Mapped(IndexOf(x -> x, _), board);
    return OneQueenPerColumnDiagonal(n, indices);
  }

  function IsEncodingValid_Indices(n : Int, bits: Bool[]) : Bool {
    let indices = Mapped(x -> BoolArrayAsInt(Reversed(x)), Chunks(BitSizeI(n - 1), bits));
    // Check that indices are valid
    for index in indices {
      if index < 0 or index >= n {
        // Message($"Incorrect index {index}");
        return false;
      }
    }
    return OneQueenPerColumnDiagonal(n, indices);
  }

  function OneQueenPerColumnDiagonal(n : Int, indices : Int[]) : Bool {
    // One queen per column and per diagonal
    for r1 in 0 .. n - 1 {
      for r2 in r1 + 1 .. n - 1 {
        let diff = indices[r1] - indices[r2];
        if diff == 0 or AbsI(diff) == r2 - r1 {
          // Message($"Queens ({r1}, {c1}) and ({r2}, {c2}) on diagonal");
          return false;
        }
      }
    }
    return true;
  }
}