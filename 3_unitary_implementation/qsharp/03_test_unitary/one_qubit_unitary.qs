namespace UnitaryImplementation {
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
}
