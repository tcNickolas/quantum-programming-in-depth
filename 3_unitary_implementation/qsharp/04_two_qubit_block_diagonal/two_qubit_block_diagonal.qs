namespace UnitaryImplementation {
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

  operation ApplyTwoQubitBlockDiagonal(
    qs : Qubit[], a : Double[][], b : Double[][]
  ) : Unit is Adj + Ctl {
    Controlled ApplyOneQubit([qs[1]], ([qs[0]], b));
    ControlledOnInt(0, ApplyOneQubit)([qs[1]], ([qs[0]], a));
  }
}
