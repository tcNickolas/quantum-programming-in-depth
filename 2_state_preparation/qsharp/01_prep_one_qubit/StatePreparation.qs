import Std.Math.ArcTan2;

@EntryPoint()
operation SingleQubitDemo() : Unit {
  use q = Qubit();
  let (alpha, beta) = (0.6, 0.8);
  let theta = ArcTan2(beta, alpha);
  Ry(2.0 * theta, q);
  Reset(q);
}
