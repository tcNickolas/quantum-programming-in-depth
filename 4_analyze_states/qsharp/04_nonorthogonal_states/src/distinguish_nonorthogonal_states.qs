namespace AnalyzeStates {
  open Microsoft.Quantum.Math;

  operation DistinguishZeroAndSup(q : Qubit, alpha : Double, beta : Double) : Int {
    // Figure out the angle of the line halfway between |0> and alpha |0> + beta |1>
    let theta = ArcTan2(beta, alpha) / 2.;
    // Rotate so that the middle between the two angles is at the angle pi/4
    Ry(- 2. * (theta - PI() / 4.), q);
    return MResetZ(q) == Zero ? 0 | 1;
  }
}
