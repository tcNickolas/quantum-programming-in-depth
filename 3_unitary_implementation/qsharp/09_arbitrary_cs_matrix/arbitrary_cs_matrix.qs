namespace UnitaryImplementation {
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Canon;
  open Microsoft.Quantum.Intrinsic;
  open Microsoft.Quantum.Logical;
  open Microsoft.Quantum.Math;

  operation ApplyOneQubit(
    qs : Qubit[], u : Double[][]
  ) : Unit is Adj + Ctl {
    if NearlyEqualD(u[0][0], -u[1][1]) and 
       NearlyEqualD(u[0][1], u[1][0]) {
      Z(qs[0]);
    }

    let angle = ArcTan2(u[1][0], u[0][0]);
    Ry(2.0 * angle, qs[0]);
  }

  operation ApplyArbitraryCSMatrix(
    qs : Qubit[], 
    cs : (Double, Double)[]
  ) : Unit is Adj + Ctl {
    for (i, (c, s)) in Enumerated(cs) {
      let m = [[c, -s], [s, c]];
      ControlledOnInt(i, ApplyOneQubit)(qs[...Length(qs) - 2], ([qs[Length(qs) - 1]], m));
    }
  }
}
