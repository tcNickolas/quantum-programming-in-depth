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

  operation TestApplyArbitraryCSMatrix(
    n : Int, cs : (Double, Double)[]
  ) : Unit {
    if Length(cs) != 2 ^ (n - 1) {
      fail "Dimensions of CS matrix don't match qubit number";
    }
    let testOp = ApplyArbitraryCSMatrix(_, cs);

    mutable completeCoefD = [];
    for (i, (c, s)) in Enumerated(cs) {
      let zBefore = [0., size = i];
      let zAfter = [0., size = 2 ^ (n - 1) - i - 1];
      set completeCoefD += 
        [zBefore + [c] + zAfter + zBefore + [-s] + zAfter];
    }
    for (i, (c, s)) in Enumerated(cs) {
      let zBefore = [0., size = i];
      let zAfter = [0., size = 2 ^ (n - 1) - i - 1];
      set completeCoefD += 
        [zBefore + [s] + zAfter + zBefore + [c] + zAfter];
    }
    let refOp = ApplyUnitaryWrap(_, completeCoefD);

    AssertOperationsEqualReferenced(n, testOp, refOp);
  }

  @Test("QuantumSimulator")
  operation TestArbitraryCSMatrix() : Unit {
    for _ in 1 .. 20 {
      let n = DrawRandomInt(2, 5);
      mutable cs = [];
      for _ in 1 .. 2 ^ (n - 1) {
        let mi = RandomOneQubitUnitary();
        set cs += [(mi[0][0], mi[1][0])];
      }
      TestApplyArbitraryCSMatrix(n, cs);
    }
  }
}