namespace NQueens {
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Convert;
  open Microsoft.Quantum.Math;
  open Microsoft.Quantum.Unstable.StatePreparation;


  // Returns the array of amplitudes of the W state on n qubits.
  function GetWStateAmps(n : Int) : Double[] {
    mutable amps = [0.0, size = 2 ^ n];
    for i in 0 .. n - 1 {
      set amps w/= (1 <<< i) <- Sqrt(1.0 / IntAsDouble(n));
    }
    return amps;
  }


  // Prepare the mean state for the bits encoding
  operation PrepareMean_Bits(n : Int, qs : Qubit[]) : Unit is Adj {
    // Prepare W state on each row of n qubits
    let wstateAmps = GetWStateAmps(n);
    for row in Chunks(n, qs) {
      PreparePureStateD(wstateAmps, row);
    }
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


  operation Oracle_Bits(n : Int, x : Qubit[], y : Qubit) : Unit {
    // The presence of a queen in row r and column c is described with x[r * n + c].
    use (validColumn, invalidRowPair) = (Qubit[n - 1], Qubit[n * (n - 1) / 2]);
    within {
      // 1. The constraint of one queen per row will be handled implicitly in search space state preparation.
      // 2. Evaluate the constraint of one queen per column.
      for c in 0 .. n - 2 {
        // Compute XOR of all qubits in this column
        for r in 0 .. n - 1 {
            CNOT(x[r * n + c], validColumn[c]);
        }
      }
      // All elements of validColumn should be 1
      // 3. Evaluate the constraint of one queen per diagonal.
      for r1 in 0 .. n - 1 {
        for r2 in r1 + 1 .. n - 1 {
          let rowPairInd = GetRowPairInd(n, r1, r2);
          // Compute AND of each pair of qubits that are on the same diagonal in these two rows.
          // Store all results in the same qubit using XOR, since at most one of the ANDs will be the 1.
          for c1 in 0 .. n - 1 {
            for c2 in [c1 + (r2 - r1), c1 - (r2 - r1)] {
              if c2 >= 0 and c2 < n {
                CCNOT(x[r1 * n + c1], x[r2 * n + c2], invalidRowPair[rowPairInd]);
              }
            }
          }
        }
      }
      // All elements of invalidRowPair should be 0 - switch them to 1 using X gates
      ApplyToEachA(X, invalidRowPair);
    } apply {
      Controlled X(validColumn + invalidRowPair, y);
    }
  }
}