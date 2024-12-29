import Std.Diagnostics.DumpMachine;
import Std.Math.ArcTan2;

@EntryPoint()
operation SingleQubitDemo() : Unit {
  use q = Qubit();
  let (alpha, beta) = (0.6, 0.8);
  let theta = 2.0 * ArcTan2(beta, alpha);
  Ry(theta, q);
  DumpMachine();
  Reset(q);
}
