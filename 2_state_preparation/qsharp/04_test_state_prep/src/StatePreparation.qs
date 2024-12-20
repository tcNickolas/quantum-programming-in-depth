import Std.Diagnostics.DumpMachine;
import Std.Math.*;

operation PrepOneQubit(q : Qubit, alpha : Double, beta : Double) : Unit
  is Adj + Ctl {
  let theta = ArcTan2(beta, alpha);
  Ry(2.0 * theta, q);
}

operation PrepTwoQubits(qs : Qubit[], a : Double[]) : Unit is Adj + Ctl {
  let b0 = Sqrt(a[0] * a[0] + a[2] * a[2]);
  let b1 = Sqrt(a[1] * a[1] + a[3] * a[3]);
  PrepOneQubit(qs[1], b0, b1);

  Controlled PrepOneQubit([qs[1]], (qs[0], a[1], a[3]));

  ApplyControlledOnInt(0, PrepOneQubit, [qs[1]], (qs[0], a[0], a[2]));
}
