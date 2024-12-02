import Std.Math.*;
import Std.Random.*;
import AnalyzeUnitaries.ReconstructUnitary;

operation ApplyOneQubit(
  q : Qubit, u : Double[][]
) : Unit is Adj + Ctl {
  if AbsD(u[0][0] - (-u[1][1])) < 1e-9 and 
      AbsD(u[0][1] - u[1][0]) < 1e-9 {
    Z(q);
  }

  let angle = ArcTan2(u[1][0], u[0][0]);
  Ry(2.0 * angle, q);
}


operation RandomOneQubitUnitary() : Double[][] {
  // Choose unitary so as to make the top left coefficient non-negative
  let theta = DrawRandomDouble(-PI() / 2., PI() / 2.);
  let sign = DrawRandomInt(0, 1) == 0 ? +1. | -1.;
  return [[Cos(theta), sign * Sin(theta)], 
          [-Sin(theta), sign * Cos(theta)]];
}


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
