namespace UnitaryImplementation {
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
}
