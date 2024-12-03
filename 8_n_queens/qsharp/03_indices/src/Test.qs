import Std.Arrays.*;
import Std.Convert.*;
import Std.Diagnostics.CheckAllZero;
import Std.Math.*;

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
    let bits = intAsEncoding(n, indicesInt);
    use (x, y) = (Qubit[Length(bits)], Qubit());
    ApplyPauliFromBitString(PauliX, true, bits, x);
    oracle(n, x, y);
    ApplyPauliFromBitString(PauliX, true, bits, x);

    let expected = isPlacementValid(n, bits);
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


// Converts int into an encoding of a queens placement.
// In "indices" mode, the queens placement is encoded using an n x bitsize Boolean array, 
// each row corresponding to an integer column index of the queen in that row
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


// Checks that the queens placement is valid.
// Since "one queen per row" is already enforced by the encoding (IntAsEncoding_Indices), 
// only checks that all columns are valid and that there is one queen per column and per diagonal
function IsPlacementValid_Indices(n : Int, bits: Bool[]) : Bool {
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


// Checks that there is one queen per column and per diagonal
// using the encoding of queens positions as indices in each row.
function OneQueenPerColumnDiagonal(n : Int, indices : Int[]) : Bool {
  // One queen per column and per diagonal
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
