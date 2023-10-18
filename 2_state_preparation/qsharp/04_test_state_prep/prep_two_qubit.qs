namespace StatePreparation {
  open Microsoft.Quantum.Canon;
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Intrinsic;
  open Microsoft.Quantum.Math;

  operation PrepOneQubit(q : Qubit, alpha : Double, beta : Double) : Unit
    is Adj + Ctl {
    let angle = ArcTan2(beta, alpha);
    Ry(2.0 * angle, q);
  }

  operation PrepTwoQubits(qs : Qubit[], a : Double[]) : Unit is Adj + Ctl {
    let b0 = Sqrt(a[0] * a[0] + a[2] * a[2]);
    let b1 = Sqrt(a[1] * a[1] + a[3] * a[3]);
    PrepOneQubit(qs[0], b0, b1);

    Controlled PrepOneQubit([qs[0]], (qs[1], a[1], a[3]));

    ControlledOnInt(0, PrepOneQubit)([qs[0]], (qs[1], a[0], a[2]));
  }

  operation PrepTwoQubitsDemo(a : Double[]) : Unit {
    use qs = Qubit[2];
    PrepTwoQubits(qs, a);
    DumpMachine();
    ResetAll(qs);
  }

  operation RunPrepTwoQubitsDemo() : Unit {
    PrepTwoQubitsDemo([0.36, 0.48, 0.64, -0.48]);
  }
}