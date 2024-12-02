import Std.Math.*;
import Std.Random.*;
import AnalyzeStates.ReconstructState;

operation PrepState(q : Qubit, alpha : Double, beta : Double) : Unit {
  Ry(2. * ArcTan2(beta, alpha), q);
}

operation TestReconstructState() : Unit {
  for _ in 1 .. 10 {
    let angle = DrawRandomDouble(0., PI() / 2.);
    let alpha = Cos(angle);
    let beta = (DrawRandomInt(0, 1) == 0 ? 1. | -1.) * Sin(angle);
    let statePrep = PrepState(_, alpha, beta);

    let (alphaRes, betaRes) = ReconstructState(statePrep);

    Message($"Actual amplitudes {alpha},{beta}, returned {alphaRes},{betaRes}");
    if AbsD(alpha - alphaRes) > 0.1 or AbsD(beta - betaRes) > 0.1 {
      fail "Incorrect amplitudes";
    }
  }
}
