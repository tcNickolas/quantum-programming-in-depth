namespace UnitaryImplementation.Test {
  open Microsoft.Quantum.Arithmetic;
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Convert;
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Math;
  open Microsoft.Quantum.Synthesis;

  open UnitaryImplementation;

  operation TestApplyTwoQubitCSMatrix(
    (c0 : Double, s0 : Double),
    (c1 : Double, s1 : Double)
  ) : Unit {
    let testOp = ApplyTwoQubitCSMatrix(_, (c0, s0), (c1, s1));

    let completeCoefD = [
      [c0, 0., -s0, 0.],
      [0., c1, 0., -s1],
      [s0, 0., c0, 0.],
      [0., s1, 0., c1]];
    let refOp = ApplyUnitaryWrap(_, completeCoefD);

    AssertOperationsEqualReferenced(2, testOp, refOp);
  }

  @Test("QuantumSimulator")
  operation TestTwoQubitCSMatrix() : Unit {
    for _ in 1 .. 20 {
      let m0 = RandomOneQubitUnitary();
      let m1 = RandomOneQubitUnitary();
      TestApplyTwoQubitCSMatrix((m0[0][0], m0[1][0]), (m1[0][0], m1[1][0]));
    }
  }
}