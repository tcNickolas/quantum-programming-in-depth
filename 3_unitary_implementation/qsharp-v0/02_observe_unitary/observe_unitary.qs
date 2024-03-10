namespace UnitaryImplementation {
  open Microsoft.Quantum.Diagnostics;
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

  @EntryPoint()
  operation SingleQubitDemo() : Unit {
    let ourOp = ApplyOneQubit(_, [[0.6, -0.8], [0.8, 0.6]]);
    DumpOperation(1, ourOp);
  }
}
