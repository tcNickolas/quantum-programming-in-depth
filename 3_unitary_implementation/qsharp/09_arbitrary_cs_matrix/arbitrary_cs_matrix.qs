namespace UnitaryImplementation {
  open Microsoft.Quantum.Arrays;
  open Microsoft.Quantum.Canon;
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Intrinsic;
  open Microsoft.Quantum.Math;

  operation ApplyOneQubit(
    qs : Qubit[], c : Double[][]
  ) : Unit is Adj + Ctl {
    if AbsD(c[1][0]) > 1E-10 and AbsD(c[1][0] - c[0][1]) < 1E-10 or 
       AbsD(c[0][0]) > 1E-10 and AbsD(c[0][0] - c[1][1]) > 1E-10 {
      Z(qs[0]);
    }

    let angle = ArcTan2(c[1][0], c[0][0]);
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
