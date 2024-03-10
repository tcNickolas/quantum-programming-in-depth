namespace UnitaryImplementation {
  open Microsoft.Quantum.Arrays;
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

  operation ApplyArbitraryCSMatrix(
    qs : Qubit[], 
    cs : (Double, Double)[]
  ) : Unit {
    for (k, (c, s)) in Enumerated(cs) {
      let m = [[c, -s], [s, c]];
      ApplyControlledOnInt(k, ApplyOneQubit, Reversed(qs[1...]),
                          ([qs[0]], m));
    }
  }
}
