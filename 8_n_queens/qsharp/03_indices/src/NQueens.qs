import Std.Arrays.*;
import Std.Convert.*;
import Std.Math.*;
import Microsoft.Quantum.Unstable.Arithmetic.*;
import Microsoft.Quantum.Unstable.StatePreparation.PreparePureStateD;


// Prepare the mean state for the indices encoding
operation PrepareMean_Indices(n : Int, qs : Qubit[]) : Unit is Adj {
  // Prepare even superposition of the first n basis states on each row of n qubits
  let meanAmps = [1.0 / Sqrt(IntAsDouble(n)), size = n];
  for row in Chunks(BitSizeI(n - 1), qs) {
    PreparePureStateD(meanAmps, row);
  }
}


// Prepare the mean state for the indices encoding - optimized version.
// Python code computes the positions of the amplitudes 
// that correspond to queen placements with one queen per column
// and passes it to Q#
operation PrepareMean_Indices_Opt(meanAmps : Double[], qs : Qubit[]) : Unit is Adj {
  PreparePureStateD(meanAmps, qs);
}


// Convert the pair of rows (row1, row2) into its integer index,
// assuming that all pairs are sorted in order of row1 increasing, then row2 increasing.
function GetRowPairInd(n : Int, row1 : Int, row2 : Int) : Int {
  mutable ind = 0;
  for r1 in 0 .. n - 1 {
    for r2 in r1 + 1 .. n - 1 {
      if r1 == row1 and r2 == row2 {
        return ind;
      }
      set ind += 1;
    }
  }
  return -1;
}


operation Oracle_Indices(n : Int, x : Qubit[], y : Qubit) : Unit {
  let bitSize = BitSizeI(n - 1);
  let indices = Chunks(bitSize, x);
  // The presence of a queen in row r and column c is described 
  // with indices[r] - bitSize bits starting with x[bitSize * r] that encode the integer c in big endian.
  use invalidRowPair = Qubit[n * (n - 1) / 2];
  within {
    // 1. The constraint of one queen per row will be handled implicitly in search space state preparation (there is only one index per row).
    // 2. Evaluate the constraint of no two queens in a column and no two queens per diagonal will be evaluated together.
    use aux = Qubit();  // The |1> bit used as MSB to keep subtraction from overflowing
    X(aux);
    for r1 in 0 .. n - 1 {
      for r2 in r1 + 1 .. n - 1 {
        let rowPairInd = GetRowPairInd(n, r1, r2);
        // Compute the difference between indices[r1] and indices[r2]
        // and check that it's not equal to 0, r1-r2, or r2-r1.
        let ind1 = Reversed([aux] + indices[r1]);
        let ind2 = Reversed(indices[r2]);
        within {
          Adjoint IncByLE(ind2, ind1);  // ind1 -= ind2
        } apply {
          for diff in [0L, IntAsBigInt(r1 - r2), IntAsBigInt(r2 - r1)] {
            ApplyIfEqualL(X, diff + (1L <<< bitSize), ind1, invalidRowPair[rowPairInd]);
          }
        }
      }
    }
    X(aux);
  } apply {
    ApplyControlledOnInt(0, X, invalidRowPair, y);
  }
}
