namespace NQueens {
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Convert;
  open Microsoft.Quantum.Math;
  open Microsoft.Quantum.Unstable.Arithmetic;
  open Microsoft.Quantum.Unstable.StatePreparation;

  function GetMeanAmps_Indices4() : Double[] {
    mutable amps = [0.0, size = 2 ^ 8];
    for ind in [27, 30, 39, 45, 54, 57, 75, 78, 99, 108, 114, 120, 135, 141, 147, 156, 177, 180, 198, 201, 210, 216, 225, 228] {
      set amps w/= ind <- 1.0;
    }
    return amps;
  }

  operation PrepareMean_Indices(n : Int, qs : Qubit[]) : Unit is Adj {
    let opt = true;
    if not opt or n != 4 {
      // Even superposition of the first n basis states
      let meanAmps = [1.0 / Sqrt(IntAsDouble(n)), size = n];
      for row in Chunks(BitSizeI(n - 1), qs) {
        PreparePureStateD(meanAmps, row);
      }
    } else {
      // Only superpositions that are permutations of distinct queen indices
      PreparePureStateD(GetMeanAmps_Indices4(), qs);
    }
  }

  operation NQueensOracle_Indices(n : Int, x : Qubit[], y : Qubit) : Unit {
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
}