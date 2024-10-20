namespace UnitaryImplementation {
  open Microsoft.Quantum.Math;

  operation ApplyOneQubit(
    qs : Qubit[], u : Double[][]
  ) : Unit is Adj + Ctl {
    if AbsD(u[0][0] - (-u[1][1])) < 1e-9 and 
       AbsD(u[0][1] - u[1][0]) < 1e-9 {
      Z(qs[0]);
    }

    let angle = ArcTan2(u[1][0], u[0][0]);
    Ry(2.0 * angle, qs[0]);
  }

  operation ApplyTwoQubitBlockDiagonal(
    qs : Qubit[], a : Double[][], b : Double[][]
  ) : Unit is Adj + Ctl {
    Controlled ApplyOneQubit([qs[0]], ([qs[1]], b));
    ApplyControlledOnInt(0, ApplyOneQubit, [qs[0]], ([qs[1]], a));
  }
}
