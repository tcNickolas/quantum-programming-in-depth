﻿namespace UnitaryImplementation {
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

  operation ApplyTwoQubitCSMatrix(
    qs : Qubit[], 
    (c0 : Double, s0 : Double),
    (c1 : Double, s1 : Double)
  ) : Unit is Adj + Ctl {
    let m0 = [[c0, -s0], [s0, c0]];
    let m1 = [[c1, -s1], [s1, c1]];
    Controlled ApplyOneQubit([qs[0]], ([qs[1]], m1));
    ControlledOnInt(0, ApplyOneQubit)([qs[0]], ([qs[1]], m0));
  }
}
