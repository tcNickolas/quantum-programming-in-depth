namespace UnitaryImplementation.Test {
  open Microsoft.Quantum.Arithmetic;
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Convert;
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Intrinsic;
  open Microsoft.Quantum.Math;
  open Microsoft.Quantum.Random;
  open Microsoft.Quantum.Synthesis;

  open UnitaryImplementation;

  operation TestApplyTwoBlockDiagonal(
    n : Int, a : Double[][], b : Double[][]
  ) : Unit {
    // For this version of the project, only test with 2 and 3 qubits.
    if n < 2 or n > 3 {
      fail "This test should run on 2- or 3-qubit unitaries";
    }

    let testOp = ApplyTwoBlockDiagonal(_, a, b);

    let zeros = [0., size = 2 ^ (n - 1)];
    mutable completeCoefD = [];
    for aRow in a {
      set completeCoefD += [aRow + zeros];
    }
    for bRow in b {
      set completeCoefD += [zeros + bRow];
    }

    let refOp = ApplyUnitaryWrap(_, completeCoefD);

    AssertOperationsEqualReferenced(n, testOp, refOp);
  }

  @Test("QuantumSimulator")
  operation TestTwoBlockDiagonalTwoQubit() : Unit {
    // Test on 2-qubit matrices (with 2x2 a and b).
    for _ in 1 .. 20 {
      let a = RandomOneQubitUnitary();
      let b = RandomOneQubitUnitary();
      TestApplyTwoBlockDiagonal(2, a, b);
    }
  }
 
  operation RandomTwoQubitBlockUnitary() : Double[][] {
    let a = RandomOneQubitUnitary();
    let b = RandomOneQubitUnitary();
    let zeros = [0., 0.];
    let u = DrawRandomBool(0.5) ?
      [a[0] + zeros,
       a[1] + zeros,
       zeros + b[0],
       zeros + b[1]] | 
      [zeros + a[0],
       zeros + a[1],
       b[0] + zeros,
       b[1] + zeros];
    return u;
  }

  @Test("QuantumSimulator")
  operation TestTwoBlockDiagonalThreeQubit() : Unit {
    // Test on 3-qubit matrices (with 4x4 a and b
    // of block-diagonal or anti-block-diagonal shape).
    for _ in 1 .. 20 {
      let a = RandomTwoQubitBlockUnitary();
      let b = RandomTwoQubitBlockUnitary();
      TestApplyTwoBlockDiagonal(3, a, b);
    }
  }
}