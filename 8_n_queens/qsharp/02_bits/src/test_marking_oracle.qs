namespace NQueens.Test {
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Convert;
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Math;
  open NQueens;

  // Helper operation to check that the given oracle recognizes valid and invalid placements.
  // intAsEncoding converts an int that encodes the placement of n queens, one per row, into the format that matches the one used by the oracle.
  // isPlacementValid checks that the placement encoded in an int is valid.
  operation AssertOracleIsValid(
    n : Int,
    intAsEncoding : (Int, Int) -> Bool[],
    oracle : (Int, Qubit[], Qubit) => Unit,
    isPlacementValid : (Int, Bool[]) -> Bool
  ) : Unit {
    // Limit the consideration to placements with one queen per row
    for indicesInt in 0 .. n ^ n - 1 {
      let encoding = intAsEncoding(n, indicesInt);
      use (x, y) = (Qubit[Length(encoding)], Qubit());
      ApplyPauliFromBitString(PauliX, true, encoding, x);
      oracle(n, x, y);
      ApplyPauliFromBitString(PauliX, true, encoding, x);

      let expected = isPlacementValid(n, encoding);
      if expected {
        X(y);
      }

      if not CheckAllZero([y]) {
        fail $"Error for x={encoding}: expected {expected}, got {not expected}";
      }
      if not CheckAllZero(x) {
        fail $"Error for x={encoding}: the state of input qubits was modified";
      }
    }
  }


  // Converts int into an encoding of a queens placement.
  // In "bits" mode, the queens placement is encoded using an n x n Boolean array, 
  // each element corresponding to a single cell of the board.
  function IntAsEncoding_Bits(n : Int, int : Int) : Bool[] {
    mutable current = int;
    mutable bits = [false, size = n * n];
    for row in 0 .. n - 1 {
      set bits w/= row * n + (current % n) <- true;
      set current /= n;
    }
    return bits;
  }


  // Checks that the queens placement is valid.
  // Since "one queen per row" is already enforced by the encoding (IntAsEncoding_Bits), 
  // converts the bits encoding into encoding of queens indices
  // and uses them to check that there is one queen per column and per diagonal
  function IsPlacementValid_Bits(n : Int, bits: Bool[]) : Bool {
    let board = Chunks(n, bits);
    let indices = Mapped(IndexOf(x -> x, _), board);
    return OneQueenPerColumnDiagonal(n, indices);
  }


  // Checks that there is one queen per column and per diagonal
  // using the encoding of queens positions as indices in each row.
  function OneQueenPerColumnDiagonal(n : Int, indices : Int[]) : Bool {
    for r1 in 0 .. n - 1 {
      for r2 in r1 + 1 .. n - 1 {
        let diff = indices[r1] - indices[r2];
        if diff == 0 {
          Message($"Queens ({r1}, {indices[r1]}) and ({r2}, {indices[r2]}) in a column");
          return false;
        }
        if AbsI(diff) == r2 - r1 {
          Message($"Queens ({r1}, {indices[r1]}) and ({r2}, {indices[r2]}) on diagonal");
          return false;
        }
      }
    }
    return true;
  }
}