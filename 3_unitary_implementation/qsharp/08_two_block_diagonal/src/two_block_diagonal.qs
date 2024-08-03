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

  operation ApplyTwoQubitBlockDiagonal(
    qs : Qubit[], a : Double[][], b : Double[][]
  ) : Unit is Adj + Ctl {
    Controlled ApplyOneQubit([qs[0]], ([qs[1]], b));
    ApplyControlledOnInt(0, ApplyOneQubit, [qs[0]], ([qs[1]], a));
  }

  operation ApplyTwoQubitCSMatrix(
    qs : Qubit[], 
    (c0 : Double, s0 : Double),
    (c1 : Double, s1 : Double)
  ) : Unit is Adj + Ctl {
    let m0 = [[c0, -s0], [s0, c0]];
    let m1 = [[c1, -s1], [s1, c1]];
    Controlled ApplyOneQubit([qs[1]], ([qs[0]], m1));
    ApplyControlledOnInt(0, ApplyOneQubit, [qs[1]], ([qs[0]], m0));
  }

  operation ApplyTwoQubitBlockAntiDiagonal(
    qs : Qubit[], a : Double[][], b : Double[][]
  ) : Unit is Adj + Ctl {
    let id = [[1., 0.], [0., 1.]];
    let minusA = [[-a[0][0], -a[0][1]], [-a[1][0], -a[1][1]]];
    ApplyTwoQubitBlockDiagonal(qs, id, minusA);
    ApplyTwoQubitCSMatrix(qs, (0., 1.), (0., 1.));
    ApplyTwoQubitBlockDiagonal(qs, id, b);
  }

  operation ApplyArbitraryUnitary(
    qs : Qubit[], u : Double[][]
  ) : Unit is Adj + Ctl {
    // We cannot implement this completely yet, 
    // but we can implement some special cases.
    let n = Length(qs);
    if n == 1 {
      ApplyOneQubit(qs, u);
    } elif n == 2 {
      // We can implement a block-diagonal or 
      // a block-anti-diagonal matrix.
      let isZeroD = x -> AbsD(x) < 1e-9;
      if All(isZeroD, 
        u[0][2..3] + u[1][2..3] + 
        u[2][0..1] + u[3][0..1]) {
        // Block-diagonal matrix.
        let tl = [u[0][0..1], u[1][0..1]];
        let br = [u[2][2..3], u[3][2..3]];
        ApplyTwoQubitBlockDiagonal(qs, tl, br);
      } elif All(isZeroD, 
        u[0][0..1] + u[1][0..1] + 
        u[2][2..3] + u[3][2..3]) {
        // Block-anti-diagonal matrix.
        let tr = [u[0][2..3], u[1][2..3]];
        let bl = [u[2][0..1], u[3][0..1]];
        ApplyTwoQubitBlockAntiDiagonal(qs, tr, bl);
      } else {
        fail "The case of arbitrary 2-qubit unitaries" +
          " is not implemented yet";
      }
    } else {
      fail "The case of 3+-qubit unitaries is not implemented yet";
    }
  }

  operation ApplyTwoBlockDiagonal(
    qs : Qubit[], a : Double[][], b : Double[][]
  ) : Unit is Adj + Ctl {
    let n = Length(qs);
    Controlled ApplyArbitraryUnitary([qs[0]], 
      (qs[1...], b));
    ApplyControlledOnInt(0, ApplyArbitraryUnitary, [qs[0]], 
      (qs[1...], a));
  }
}
