namespace AnalyzeUnitaries.Test {
  open Microsoft.Quantum.Convert;
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Intrinsic;
  open Microsoft.Quantum.Logical;
  open Microsoft.Quantum.Math;
  open Microsoft.Quantum.Random;
  open AnalyzeUnitaries;

  operation ApplyOneQubit(
    q : Qubit, u : Double[][]
  ) : Unit is Adj + Ctl {
    if NearlyEqualD(u[0][0], -u[1][1]) and 
       NearlyEqualD(u[0][1], u[1][0]) {
      Z(q);
    }

    let angle = ArcTan2(u[1][0], u[0][0]);
    Ry(2.0 * angle, q);
  }

  operation RandomOneQubitUnitary() : Double[][] {
    // Choose unitary so as to make the top left coefficient non-negative
    let theta = DrawRandomDouble(-PI() / 2., PI() / 2.);
    let sign = DrawRandomBool(0.5) ? +1. | -1.;
    return [[Cos(theta), sign * Sin(theta)], 
           [-Sin(theta), sign * Cos(theta)]];
  }

  @Test("QuantumSimulator")
  operation TestReconstructUnitary() : Unit {
    for _ in 1 .. 10 {
      let matrix = RandomOneQubitUnitary();
      let unitary = ApplyOneQubit(_, matrix);
      let matrixRes = ReconstructUnitary(unitary);

      Message($"Actual matrix {matrix}, returned {matrixRes}");
      for j in 0 .. 1 {
        for k in 0 .. 1 {
          if AbsD(matrix[j][k] - matrixRes[j][k]) > 0.1 {
            fail $"Incorrect coefficient at [{j}][{k}]: expected {matrix[j][k]}, got {matrixRes[j][k]}";
          }
        }
      }
    }
  }
}