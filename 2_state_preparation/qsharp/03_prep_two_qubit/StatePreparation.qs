﻿import Std.Diagnostics.DumpMachine;
import Std.Math.ArcTan2, Std.Math.Sqrt;

operation PrepOneQubit(q : Qubit, alpha : Double, beta : Double) : Unit
  is Adj + Ctl {
  let theta = 2.0 * ArcTan2(beta, alpha);
  Ry(theta, q);
}

operation PrepTwoQubits(qs : Qubit[], a : Double[]) : Unit is Adj + Ctl {
  let b0 = Sqrt(a[0] * a[0] + a[2] * a[2]);
  let b1 = Sqrt(a[1] * a[1] + a[3] * a[3]);
  PrepOneQubit(qs[1], b0, b1);

  Controlled PrepOneQubit([qs[1]], (qs[0], a[1], a[3]));

  ApplyControlledOnInt(0, PrepOneQubit, [qs[1]], (qs[0], a[0], a[2]));
}

operation PrepTwoQubitsDemo(a : Double[]) : Unit {
  use qs = Qubit[2];
  PrepTwoQubits(qs, a);
  DumpMachine();
  ResetAll(qs);
}

@EntryPoint()
operation RunPrepTwoQubitsDemo() : Unit {
  PrepTwoQubitsDemo([0.36, 0.48, 0.64, -0.48]);
}
