namespace StatePreparation {
  open Microsoft.Quantum.Diagnostics;
  open Microsoft.Quantum.Math;

  @EntryPoint()
  operation SingleQubitDemo() : Unit {
    use q = Qubit();
    let (alpha, beta) = (0.6, 0.8);
    let angle = ArcTan2(beta, alpha);
    Ry(2.0 * angle, q);
    DumpMachine();
    Reset(q);
  }
}
