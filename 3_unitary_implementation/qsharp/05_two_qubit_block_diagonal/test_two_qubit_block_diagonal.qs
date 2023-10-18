namespace UnitaryImplementation.Test {
  open Microsoft.Quantum.Arithmetic;
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Convert;
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Math;
  open Microsoft.Quantum.Synthesis;

  open UnitaryImplementation;

  operation TestApplyTwoQubitBlockDiagonal(
    a : Double[][], b : Double[][]
  ) : Unit {
    ValidateOneQubitUnitary(a);
    ValidateOneQubitUnitary(b);

    let testOp = ApplyTwoQubitBlockDiagonal(_, a, b);

    let completeCoefD = [
      a[0] + [0., 0.],
      a[1] + [0., 0.],
      [0., 0.] + b[0],
      [0., 0.] + b[1]];
    let refOp = ApplyUnitaryWrap(_, completeCoefD);

    AssertOperationsEqualReferenced(2, testOp, refOp);
  }

  @Test("QuantumSimulator")
  operation TestTwoQubitBlockDiadonal() : Unit {
    for _ in 1 .. 20 {
      let a = RandomOneQubitUnitary();
      let b = RandomOneQubitUnitary();
      TestApplyTwoQubitBlockDiagonal(a, b);
    }
  }
}